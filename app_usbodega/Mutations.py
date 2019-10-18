import graphene

from app_usbodega.Catalogo import Catalogo
from .Categoria import Categoria
from .Medida import Medida
from .Register import Register, Logout, AddProducto


class Mutation(graphene.ObjectType):
    register = Register.Field()
    addproducto = AddProducto.Field()
    addmedida = Medida.Field()
    addcategoria = Categoria.Field()
    addcatalogo = Catalogo.Field()
    logout = Logout.Field()
