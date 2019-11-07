import graphene

from app_usbodega.Areas import AreasQuery
from app_usbodega.Beneficiario import QueriesBeneficiario
from app_usbodega.graphql.queries.CurrentCatalogo import CurrentCatalogoQueries
from app_usbodega.Cargos import QueriesCargo
from app_usbodega.graphql.hibrido.Catalogo import LastCatalogo
from app_usbodega.graphql.queries.Login import Login
from app_usbodega.graphql.queries.localCatalogos import LocalCatalogo


class Query(Login, LastCatalogo, AreasQuery, QueriesCargo,
            QueriesBeneficiario, LocalCatalogo, CurrentCatalogoQueries, graphene.ObjectType):
    pass
