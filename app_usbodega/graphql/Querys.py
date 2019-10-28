import graphene

from app_usbodega.graphql.hibrido.Catalogo import LastCatalogo
from app_usbodega.graphql.queries.Login import Login


class Query(Login, LastCatalogo, graphene.ObjectType):
    pass
