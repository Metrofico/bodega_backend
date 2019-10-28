import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from app_usbodega.graphql.Inputs import InputAddCategorias
from app_usbodega.models import Categoria as CategoriaModel


class Categoria(graphene.Mutation):
    class Arguments:
        addcategoria = InputAddCategorias(required=True)

    codigo = graphene.String(required=True)
    nombre = graphene.String(required=True)

    def mutate(self, info, addcategoria):
        codigo = str(addcategoria.codigo).strip()
        nombre = str(addcategoria.nombre).strip()

        try:
            CategoriaModel.objects.get(codigo=codigo)
            raise Exception("Los datos ya existen")
        except ObjectDoesNotExist:
            categoria = CategoriaModel(codigo=codigo, categoria=nombre)
            try:
                categoria.save()
            except IntegrityError as error:
                raise Exception("Error de integridad de categoria")
            return Categoria(codigo=codigo, nombre=nombre)
