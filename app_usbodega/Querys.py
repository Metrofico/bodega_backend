import graphene

from .Login import Login
from .Beneficiario import Beneficiario
from .Areas import AreasQuery


class Query(Login, AreasQuery, graphene.ObjectType):
    pass
