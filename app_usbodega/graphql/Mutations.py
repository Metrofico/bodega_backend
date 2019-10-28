import graphene

from app_usbodega.graphql.hibrido.Catalogo import Catalogo
from app_usbodega.graphql.mutations.Categoria import Categoria
from app_usbodega.graphql.mutations.Register import Register, Logout, AddProducto


class Mutation(graphene.ObjectType):
    register = Register.Field()
    addproducto = AddProducto.Field()
    addcategoria = Categoria.Field()
    addcatalogo = Catalogo.Field()
    logout = Logout.Field()
