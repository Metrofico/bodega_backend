import graphene

from .Register import Register, Logout, AddProducto


class Mutation(graphene.ObjectType):
    register = Register.Field()
    addproducto = AddProducto.Field()
    logout = Logout.Field()
