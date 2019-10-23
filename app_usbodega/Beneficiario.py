import graphene
from django.contrib.postgres.search import SearchVector, SearchQuery
from .Inputs import InputRegisterBeneficiario, InputBeneficiarioQuery, InputUpdateBeneficiario
from .utils.GeneralDataValidation import verificar, strfilters, has_value
from .utils.Date import Date
from .models import Areas, Cargos, Beneficiario
from .ObjectsTypes import BeneficiarioType


class QueriesBeneficiario(graphene.ObjectType):
    query_beneficiarios = graphene.List(BeneficiarioType, data=InputBeneficiarioQuery())

    @staticmethod
    def resolve_query_beneficiarios(self, info, data):
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
    beneficiarios_fields = (
        "tipo_doc", "documento", "nombres", "apellido_paterno", "apellido_materno", "fecha_registro",
        "area_id", "cargo_id", "telefono")

    class Arguments:
        mType = graphene.String(required=True)
        create = InputRegisterBeneficiario()
        update = InputUpdateBeneficiario()

    response = graphene.Boolean()

    def is_a_valid_field(self, field):
        coincidence = 0
        for item in self.beneficiarios_fields:
            if item == field:
                coincidence += 1
        return True if coincidence > 0 else False

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
            has_value(apellido_paterno, "Apellido paterno")
            has_value(apellido_materno, "Apellido Paterno")
            has_value(area, "Area")
            has_value(cargo, "Cargo")
            has_value(telefono, "Telefono")

            if tipo_doc > 2 or tipo_doc == 0:
                raise Exception("Tipo de documento invalido, indices validos: 1 (Cédula), 2 (Pasaporte)")
            else:
                tipo_doc_str = "Cédula" if tipo_doc == 1 else "Pasaporte"

            if verificar(documento):
                data1 = Areas.objects.filter(id=area)
                data2 = Cargos.objects.filter(id=cargo)
                if data1.count() != 0 and data2.count() != 0:
                    fecha = Date.get_full_date()
                    insercion = Beneficiario(tipo_doc=tipo_doc_str, documento=documento, nombres=nombres,
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
            update = kwargs["update"]
            field = update.field.strip()
            new_value = update.new_value.strip()
            if not self.is_a_valid_field():
                raise Exception(
                    "El campo '" + field + "' no es valido: los validos son " + str(self.beneficiarios_fields))
            has_value(new_value, "new_value")
            Beneficiario.objects.filter(id=update.id).update(**{field: new_value})
            return MutateBeneficiario(response=True)
        elif mType == "delete":
            pass
        else:
            raise Exception(
                "¡Valor invalido para mType!, las operaciones permitidas son: 'create', 'update' y 'delete'")
