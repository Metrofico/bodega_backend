import graphene
from app_usbodega.utils.GeneralDataValidation import strfilters
from .models import Cargos
from .ObjectsTypes import CargosType


def exists_cargo(cargo):
    data = Cargos.objects.filter(cargo=cargo)
    return data.count() != 0


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
        q_type = str.lower(kwargs["qType"])
        to_return = []
        if q_type == "filter":
            data = Cargos.objects.filter(cargo__startswith=str.upper(kwargs["cargo"]))
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
        cargo = graphene.String(required=True)
        old_cargo = graphene.String()

    response = graphene.Boolean()

    @staticmethod
    def mutate(self, info, **kwargs):
        cargo = str.upper(kwargs["cargo"])
        m_type = kwargs["mType"]
        exist = True
        check_filters(cargo)
        operation = str.lower(m_type)
        if operation == "update":
            old_cargo = str.upper(kwargs["old_cargo"])
            if exists_cargo(old_cargo):
                check_filters(old_cargo)
                Cargos.objects.filter(cargo=old_cargo).update(cargo=cargo)
            else:
                print("NO Existe el cargo: " + str(old_cargo))
                exist = False
        elif operation == "delete":
            if exists_cargo(cargo):
                Cargos.objects.filter(cargo=cargo).delete()
            else:
                exist = False
        elif operation == "create":
            if not exists_cargo(cargo):
                Cargos(cargo=cargo).save()
            else:
                raise Exception("El cargo ya existe")
        else:
            raise Exception("Tipo de operacion invalida, las permitidas son: create, update, delete")

        if exist:
            return MutateCargo(response=True)
        else:
            raise Exception("El cargo no existe")
