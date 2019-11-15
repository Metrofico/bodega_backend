import graphene
from django.contrib.postgres.search import SearchVector

from app_usbodega.graphql.objetos.ObjectsTypes import CategoriaModel
from app_usbodega.models import Categoria


class QCategoria(graphene.AbstractType):
    list_categorias = graphene.List(CategoriaModel, filter_data=graphene.String())

    def resolve_list_categorias(self, info, **kwargs):
        if "filter_data" in kwargs:
            filter_data = str(kwargs["filter_data"]).lower()
            if str(filter_data).strip():
                db_awnser = Categoria.objects.annotate(
                    search=SearchVector("codigo", "categoria")).filter(
                    search__icontains=filter_data)
                return [CategoriaModel(id=categoria.id, codigo=categoria.codigo, descripcion=categoria.categoria) for
                        categoria
                        in
                        db_awnser.order_by("codigo")]
        return [CategoriaModel(id=categoria.id, codigo=categoria.codigo, descripcion=categoria.categoria) for categoria
                in
                Categoria.objects.all().order_by("codigo")]
