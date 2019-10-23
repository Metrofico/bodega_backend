import graphene
from django.contrib.postgres.search import SearchVector
from .Inputs import InputRegisterBeneficiario, InputBeneficiarioQuery, InputUpdateBeneficiario
from .utils.GeneralDataValidation import verificar, get_tipo_documento, has_value, exists_field
from .utils.Date import Date
from .models import Areas, Cargos, Beneficiario
from .ObjectsTypes import BeneficiarioType
#dsad

class QueriesBeneficiario(graphene.ObjectType):
    query_beneficiarios = graphene.List(BeneficiarioType, data=InputBeneficiarioQuery())

    @staticmethod
    def resolve_query_beneficiarios(slef, info, data):
        q_type = str.lower(data.qType).strip()
        if q_type == "all":
            db_awnser = Beneficiario.objects.all()
        elif q_type == "filter":
            beneficiario = str(data.beneficiario).strip()
            if beneficiario == "":
                raise Exception("¡El campo beneficiario esta vacio!")
            db_awnser = Beneficiario.objects.annotate(
                search=SearchVector('nombres', 'apellido_paterno')).filter(
                search__icontains=beneficiario)
        else:
            raise Exception("¡Valor invalido para qType!, las operaciones permitidas son: 'filter' y 'all'")

        to_return = []
        for item in db_awnser:
            to_return.append(BeneficiarioType(id=item.id, tipo_doc=item.tipo_doc, documento=item.documento,
                                              nombres=item.nombres, apellido_paterno=item.apellido_paterno,
                                              apellido_materno=item.apellido_materno, area=item.area.area,
                                              cargo=item.cargo.cargo, telefono=item.telefono,
                                              fecha_registro=item.fecha_registro,
                                              fecha_modificacion=item.fecha_modificacion))
        return to_return


class MutateBeneficiario(graphene.Mutation):
    class Arguments:
        mType = graphene.String(required=True)
        target = graphene.Int()
        create = InputRegisterBeneficiario()
        update = InputUpdateBeneficiario()

    response = graphene.Boolean()

    @staticmethod
    def mutate(self, info, mType, **kwargs):
        mType = str.lower(mType)
        if mType == "create":
            create = kwargs["create"]
            tipo_doc = create.tipo_doc
            documento = create.documento.strip()
            nombres = create.nombres.strip()
            apellido_paterno = create.apellido_paterno.strip()
            apellido_materno = create.apellido_materno.strip()
            area = create.area
            cargo = create.cargo
            telefono = create.telefono.strip()
            has_value(tipo_doc, "Tipo de documento")
            has_value(documento, "Número de documento")
            has_value(nombres, "Nombres")
            has_value(apellido_paterno, "Apellido paterno")
            has_value(apellido_materno, "Apellido Paterno")
            has_value(area, "Area")
            has_value(cargo, "Cargo")
            has_value(telefono, "Teléfono")

            tipo_doc = get_tipo_documento(tipo_doc)

            if verificar(documento):
                data1 = Areas.objects.filter(id=area)
                data2 = Cargos.objects.filter(id=cargo)
                if data1.count() != 0 and data2.count() != 0:
                    fecha = Date.get_full_date()
                    insercion = Beneficiario(tipo_doc=tipo_doc, documento=documento, nombres=nombres,
                                             apellido_paterno=apellido_paterno,
                                             apellido_materno=apellido_materno,
                                             area=Areas(id=area), cargo=Cargos(id=cargo), fecha_registro=fecha,
                                             telefono=telefono)
                    insercion.save()
                    return MutateBeneficiario(response=True)
                elif data1.count() == 0:
                    raise Exception("El area ingresada no es valida")
                else:
                    raise Exception("El cargo ingresado no es valido")
            else:
                raise Exception("El número de documento es invalido")
        elif mType == "update":
            vals = {}
            update = kwargs["update"]
            target = update.target
            if not exists_field(model=Beneficiario, field="id", dato=target, upper_case=False):
                raise Exception("¡El beneficiario indicado no existe!")
            tipo_doc = update.tipo_doc
            documento = update.documento
            nombres = update.nombres
            apellidos_paterno = update.apellido_paterno
            apellidos_materno = update.apellido_materno
            telefono = update.telefono
            area = update.area
            cargo = update.cargo

            if tipo_doc is not None:
                has_value(tipo_doc, "Tipo de documento")
                vals["tipo_doc"] = get_tipo_documento(tipo_doc)
            if documento is not None:
                documento = documento.strip()
                has_value(documento, "Número de documento")
                if verificar(documento):
                    vals["documento"] = documento
                else:
                    raise Exception("¡El número de documento no es valido!")
            if nombres is not None:
                nombres = nombres.strip()
                has_value(nombres, "Nombres")
                vals["nombres"] = nombres
            if apellidos_paterno is not None:
                apellidos_paterno = apellidos_paterno.strip()
                has_value(apellidos_paterno, "Apellido paterno")
                vals["apellido_paterno"] = apellidos_paterno
            if apellidos_materno is not None:
                apellidos_materno = apellidos_materno.strip()
                has_value(apellidos_materno, "Apellido materno")
                vals["apellido_materno"] = apellidos_materno
            if telefono is not None:
                telefono = telefono.strip()
                has_value(telefono, "Télefono")
                vals["telefono"] = telefono
            if area is not None:
                has_value(area, "Area")
                if exists_field(model=Areas, field="id", dato=area, upper_case=False):
                    vals["area"] = area
                else:
                    raise Exception("¡El area indicada no existe!")
            if cargo is not None:
                has_value(cargo, "Cargo")
                if exists_field(model=Cargos, field="id", dato=cargo, upper_case=False):
                    vals["cargo"] = cargo
                else:
                    raise Exception("¡El cargo indicado no existe!")
            fecha_update = Date.get_full_date()
            vals["fecha_modificacion"] = fecha_update
            Beneficiario.objects.filter(id=target).update(**vals)
            return MutateBeneficiario(response=True)
        elif mType == "delete":
            try:
                target = kwargs["target"]
            except Exception:
                raise Exception(
                    "La operacion 'delete' requiere el envio del id del beneficiario en el parametro 'target' de la "
                    "query")
            if not exists_field(Beneficiario, "id", target, False):
                raise Exception("!El beneficiario indicado no existe!")
            Beneficiario.objects.filter(id=target).delete()
            return MutateBeneficiario(response=True)
            pass
        else:
            raise Exception(
                "¡Valor invalido para mType!, las operaciones permitidas son: 'create', 'update' y 'delete'")
