import graphene
from app_usbodega.utils.GeneralDataValidation import strfilters, exists_field
from .models import Cargos
from .ObjectsTypes import CargosType
from .Inputs import InputRegisterCargo, InputUpdateCargo, InputDeleteCargo


def check_filters(cargo):
    strfilters(str=cargo, min_length=5,
               errormessageminlength="¡La cantidad de caracteres minima permitida para el/los cargo es de 5",
               max_length=100,
               errormessagemaxlength="!La cantidad de caracteres maxima para el/los cargo es de 100")


class QueriesCargo(graphene.ObjectType):
    query_cargo = graphene.List(CargosType, qType=graphene.String(required=True),
                                cargo=graphene.String(required=False))

    @staticmethod
    def resolve_query_cargo(self, info, **kwargs):
        q_type = str.lower(kwargs["qType"]).strip()
        to_return = []
        if q_type == "filter":
            cargo = kwargs["cargo"].strip();
            data = Cargos.objects.filter(cargo__startswith=str.upper(cargo))
        elif q_type == "all":
            data = Cargos.objects.all()
        else:
            raise Exception("Tipo de operacion invalida, las permitidas son: 'filter' y 'all'")
        for item in data:
            to_return.append(CargosType(id=item.id, cargo=item.cargo))
        return to_return


class MutateCargo(graphene.Mutation):
    class Arguments:
        mType = graphene.String(required=True)
        update = InputUpdateCargo()
        create = InputRegisterCargo()
        delete = InputDeleteCargo()

    response = graphene.Boolean()

    @staticmethod
    def mutate(self, info, **kwargs):
        m_type = kwargs["mType"].strip()
        exist = True
        operation = str.lower(m_type)
        if operation == "update":
            try:
                update = kwargs["update"]
            except Exception:
                raise Exception("!Debe incluir el argumento 'update' , para llevar a cabo esta operación!")
            target = update.target
            if exists_field(model=Cargos, field="id", dato=target, upper_case=False):
                cargo = update.cargo
                check_filters(cargo)
                Cargos.objects.filter(id=target).update(cargo=cargo)
            else:
                exist = False
        elif operation == "delete":
            try:
                delete = kwargs["delete"]
            except Exception:
                raise Exception("!Debe incluir el argumento 'delete' , para llevar a cabo esta operación!")
            target = delete.target

            if exists_field(model=Cargos, field="id", dato=target, upper_case=False):
                Cargos.objects.filter(id=target).delete()
            else:
                exist = False

        elif operation == "create":
            try:
                create = kwargs["create"]
            except Exception:
                raise Exception("!Debe incluir el argumento 'create' , para llevar a cabo esta operación!")
            cargo = str.upper(create.cargo)
            check_filters(cargo)
            if not exists_field(model=Cargos, field="cargo", dato=cargo, upper_case=True):
                Cargos(cargo=cargo).save()
            else:
                raise Exception("El cargo ya existe")
        else:
            raise Exception("Tipo de operacion invalida, las permitidas son: create, update, delete")

        if exist:
            return MutateCargo(response=True)
        else:
            raise Exception("No existe el cargo")
