import graphene

from .Register import Register, Logout


class Mutation(graphene.ObjectType):
    register = Register.Field()
    logout = Logout.Field()
