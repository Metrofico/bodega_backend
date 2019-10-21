import graphene

from app_usbodega.Mutations import Mutation
from app_usbodega.Querys import Query


class Mutations(Mutation, graphene.ObjectType):
    pass


class Querys(Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Querys, mutation=Mutations, auto_camelcase=False)
