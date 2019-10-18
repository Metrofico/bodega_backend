import graphene

from .Register import Register, Logout, AddProducto
from .Areas import AddArea, DeleteArea, UpdateArea


class Mutation(graphene.ObjectType):
    register = Register.Field()
    addproducto = AddProducto.Field()
    logout = Logout.Field()
    addArea = AddArea.Field()
    deleteArea = DeleteArea.Field()
    updateArea = UpdateArea.Field()
