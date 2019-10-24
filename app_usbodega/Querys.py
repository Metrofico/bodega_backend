import graphene

from app_usbodega.Catalogo import LastCatalogo
from .Login import Login


class Query(Login, LastCatalogo, graphene.ObjectType):
    pass
