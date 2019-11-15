import graphene
from django.core.exceptions import ObjectDoesNotExist

from app_usbodega.graphql.objetos.ObjectsTypes import ArticuloType, CurrentCatalogoObj, CategoriaModel
from app_usbodega.models import Articulo, Categoria, CurrentCatalogo


class AddArticulo(graphene.Mutation):
    class Arguments:
        id_catalogo = graphene.Int()
        id_categoria = graphene.Int()

    success = graphene.String()

    def mutate(self, info, id_catalogo, id_categoria):
        try:
            catalogo = CurrentCatalogo.objects.get(id=id_catalogo)
        except ObjectDoesNotExist:
            raise Exception("El item del catálogo no existe")
        try:
            categoria = Categoria.objects.get(id=id_categoria)
        except ObjectDoesNotExist:
            raise Exception("La categoría no existe")
        if Articulo.objects.filter(id_de_existencia=catalogo.id_de_existencia).count() > 0:
            raise Exception("Ya existe un articulo con el mismo nombre")
        articulo = Articulo(id_de_existencia=catalogo.id_de_existencia, descripcion=catalogo.descripcion,
                            item_presupuestario=catalogo.item_presupuestario, id_categoria=categoria)
        articulo.save()
        return AddArticulo(success="ok")


class GetArticulo(graphene.AbstractType):
    list_articulo = graphene.List(ArticuloType)

    def resolve_list_articulo(self, info):
        articulos = []
        articulos_fetch = Articulo.objects.all()
        for item in articulos_fetch:
            articulos.append(ArticuloType(id=item.id,
                                          id_de_existencia=item.id_de_existencia,
                                          descripcion=item.descripcion,
                                          item_presupuestario=item.item_presupuestario,
                                          categoria=CategoriaModel(
                                              id=item.id_categoria.id,
                                              codigo=item.id_categoria.codigo,
                                              descripcion=item.id_categoria.categoria
                                          )))
        return articulos
