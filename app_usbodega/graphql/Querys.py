import graphene

from app_usbodega.Areas import AreasQuery
from app_usbodega.Beneficiario import QueriesBeneficiario
from app_usbodega.Cargos import QueriesCargo
from app_usbodega.graphql.hibrido.Catalogo import LastCatalogo
from app_usbodega.graphql.queries.Login import Login


class Query(Login, LastCatalogo, AreasQuery, QueriesCargo, QueriesBeneficiario, graphene.ObjectType):
    pass
