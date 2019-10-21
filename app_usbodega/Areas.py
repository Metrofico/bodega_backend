import graphene
from .models import Areas
from .ObjectsTypes import AreasType
from .filters import *


def exists_area(area):
    data = Areas.objects.filter(area=str.upper(area))
    return data.count() != 0


class AreasQuery(graphene.ObjectType):
    get_areas = graphene.List(AreasType)
    search_area = graphene.List(AreasType, parameter=graphene.String())

    def resolve_get_areas(self, info):
        data = Areas.objects.all()
        retorno = []
        for item in data:
            retorno.append(AreasType(id=item.id, area=item.area))
        return retorno

    def resolve_search_area(self, info, parameter):
        data = Areas.objects.filter(area__startswith=str.upper(parameter))
        retorno = []
        for item in data:
            retorno.append(AreasType(id=item.id, area=item.area))
        return retorno


class AddArea(graphene.Mutation):
    class Arguments:
        area = graphene.String(required=True)

    response = graphene.Boolean()

    def mutate(self, info, area):
        strfilters(str=area, min_length=5,
                   errormessageminlength="¡La cantidad de caracteres minima permitida para el area es de 5",
                   max_length=100, errormessagemaxlength="!La cantidad de caracteres maxima para el area es de 100")
        if not exists_area(area):
            insert = Areas(area=str.upper(area))
            insert.save()
            return AddArea(response=True)
        else:
            raise Exception("¡El area que desea añadir ya existe!")


class DeleteArea(graphene.Mutation):
    class Arguments:
        area = graphene.String(required=True)

    response = graphene.Boolean()

    def mutate(self, info, area):
        if exists_area(area):
            Areas.objects.filter(area=str.upper(area)).delete()
            return DeleteArea(response=True)
        else:
            raise Exception("!El area que desea eliminar no existe!")


class UpdateArea(graphene.Mutation):
    class Arguments:
        old_area = graphene.String(required=True)
        new_area = graphene.String(required=True)

    response = graphene.Boolean()

    def mutate(self, info, old_area, new_area):
        strfilters(str=old_area, min_length=5,
                   errormessageminlength="¡La cantidad de caracteres minima permitida para el area anterior es de 5",
                   max_length=100,
                   errormessagemaxlength="!La cantidad de caracteres maxima para el area anterior es de 100")
        strfilters(str=new_area, min_length=10,
                   errormessageminlength="¡La cantidad de caracteres minima permitida para la nueva area es de 10",
                   max_length=100,
                   errormessagemaxlength="!La cantidad de caracteres maxima para el area nueva es de 255")

        if exists_area(old_area):
            Areas.objects.filter(area=str.upper(old_area)).update(area=str.upper(new_area))
            return UpdateArea(response=True)
        else:
            raise Exception("!El area que desea eliminar no existe!")
        pass
