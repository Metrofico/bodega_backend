import graphene

from .Login import Login


class Query(Login, graphene.ObjectType):
    pass
