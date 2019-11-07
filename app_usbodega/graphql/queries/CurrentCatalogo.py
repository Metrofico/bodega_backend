import graphene
from django.contrib.postgres.search import SearchVector
from ...utilidades.GeneralDataValidation import has_value, min_length, check_empty
from ..objetos.ObjectsTypes import CurrentCatalogoObj
from ...models import CurrentCatalogo


class CurrentCatalogoQueries(graphene.ObjectType):
    query_ccatalogo = graphene.List(CurrentCatalogoObj, searcher=graphene.String(required=True))

    def resolve_query_ccatalogo(self, info, searcher):
        check_empty(searcher)
        min_length(searcher, 4, "El criterio de busqueda debe tener minimo 4 caracteres")
        to_return = []
        db_awnser = CurrentCatalogo.objects.annotate(
            search=SearchVector("id_de_existencia", "descripcion", "item_presupuestario")).filter(
            search__icontains=searcher)

        for item in db_awnser:
            item_presupuestario = "" if item.item_presupuestario == "None" else item.item_presupuestario
            to_return.append(CurrentCatalogoObj(id_existencia=item.id_de_existencia, descripcion=item.descripcion,
                                                item_presupuestario=item_presupuestario))
        return to_return
