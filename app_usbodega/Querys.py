import graphene

from .Login import Login
from .Areas import AreasQuery
from .Cargos import QueriesCargo
from .Beneficiario import QueriesBeneficiario


class Query(Login, AreasQuery, QueriesCargo, QueriesBeneficiario, graphene.ObjectType):
    pass
