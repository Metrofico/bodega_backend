import graphene

from app_usbodega.graphql.objetos.ObjectsTypes import CatalogoList
from app_usbodega.models import Catalogos


class LocalCatalogo(graphene.AbstractType):
    list_local_catalogos = graphene.List(CatalogoList)

    def resolve_list_local_catalogos(self, info):
        catalogos_local = []
        catalogos = Catalogos.objects.all()
        if catalogos.count() < 1:
            return catalogos_local
        for Catalogo in catalogos:
            catalogos_local.append(
                CatalogoList(id=Catalogo.id,
                             nombre=(Catalogo.nameFile.rstrip(".pdf")[:Catalogo.nameFile.rstrip(".pdf").rfind("-")]),
                             subida=str(Catalogo.date_uploaded)))
        # catalogos_local.append(CatalogoList(nombre=""))
        # catalogos_local.append(CatalogoList(nombre=""))
        return catalogos_local
