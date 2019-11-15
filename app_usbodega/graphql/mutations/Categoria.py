import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from app_usbodega.graphql.Inputs import InputAddCategorias
from app_usbodega.models import Categoria as CategoriaModel


class RemoveCategoria(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    codigo = graphene.String()
    descripcion = graphene.String()

    def mutate(self, info, **kwargs):
        identificador_categoria = kwargs["id"]
        try:
            categoria = CategoriaModel.objects.get(id=identificador_categoria)
            codigo = categoria.codigo
            descripcion = categoria.categoria
            categoria.delete()
        except ObjectDoesNotExist:
            raise Exception("No existe la categoria que desea remover")
        return RemoveCategoria(codigo=codigo, descripcion=descripcion)


class EditCategoria(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        codigo = graphene.String()
        descripcion = graphene.String()

    codigo = graphene.String()
    descripcion = graphene.String()

    def mutate(self, info, **kwargs):
        categoria_id = kwargs["id"]
        categoria_codigo_nuevo = ""
        categoria_descripcion_nuevo = ""
        try:
            categoria = CategoriaModel.objects.get(id=categoria_id)
            if "codigo" in kwargs:
                categoria_codigo_nuevo = kwargs["codigo"]
                if str(categoria_codigo_nuevo).strip():
                    categoria_f = CategoriaModel.objects.filter(codigo=categoria_codigo_nuevo).count()
                    if categoria_f > 0:
                        raise Exception("El código ya existe en una categoria registrada")
                    categoria.codigo = categoria_codigo_nuevo
            if "descripcion" in kwargs:
                categoria_descripcion_nuevo = kwargs["descripcion"]
                if str(categoria_descripcion_nuevo).strip():
                    categoria_f = CategoriaModel.objects.filter(categoria=categoria_descripcion_nuevo).count()
                    if categoria_f > 0:
                        raise Exception("La descripción ya existe en una categoria registrada")
                    categoria.categoria = categoria_descripcion_nuevo
            categoria.save()
        except ObjectDoesNotExist:
            raise Exception("La categoria no existe!")
        return EditCategoria(codigo=categoria_codigo_nuevo, descripcion=categoria_descripcion_nuevo)


class Categoria(graphene.Mutation):
    class Arguments:
        addcategoria = InputAddCategorias(required=True)

    id = graphene.String()
    codigo = graphene.String(required=True)
    nombre = graphene.String(required=True)

    def mutate(self, info, addcategoria):
        codigo = str(addcategoria.codigo).strip().replace("\t", "")
        nombre = str(addcategoria.nombre).strip().replace("\t", "")
        if not codigo:
            raise Exception("Escriba un código unico para su categoria")
        if not nombre:
            raise Exception("Escriba una descripción unica para su categoria")
        try:
            CategoriaModel.objects.get(codigo=codigo)
            raise Exception("Debe escribir un código que no exista en los registros")
        except ObjectDoesNotExist:
            try:
                CategoriaModel.objects.get(categoria=nombre)
                raise Exception("Debe escribir un nombre de categoria que no exista en los registros")
            except ObjectDoesNotExist:
                categoria = CategoriaModel(codigo=codigo, categoria=nombre)
                try:
                    categoria.save()
                except IntegrityError as error:
                    raise Exception("Error de integridad de categoria")
                return Categoria(id=categoria.id, codigo=codigo, nombre=nombre)
