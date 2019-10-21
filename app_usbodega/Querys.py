import graphene

from .Login import Login
from .Beneficiario import Beneficiario
from .Areas import AreasQuery
from .Cargos import queriesCargo


class Query(Login, AreasQuery, queriesCargo, graphene.ObjectType):
    pass
