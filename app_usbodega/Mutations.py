import graphene

from .Register import Register


class Mutation(graphene.ObjectType):
    register = Register.Field()
