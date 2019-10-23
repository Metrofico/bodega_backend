import graphene

from app_usbodega.Catalogo import Catalogo
from .Categoria import Categoria
from .Register import Register, Logout, AddProducto


class Mutation(graphene.ObjectType):
    register = Register.Field()
    addproducto = AddProducto.Field()
    addcategoria = Categoria.Field()
    addcatalogo = Catalogo.Field()
    logout = Logout.Field()
