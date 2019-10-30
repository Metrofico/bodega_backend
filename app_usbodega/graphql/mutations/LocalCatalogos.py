import graphene
from app_usbodega.models import Catalogos


class RemoveDataCatalogo(graphene.Mutation):
    class Arguments:
        uid = graphene.String(required=True)

    success = graphene.String()

    def mutate(self, info, uid):
        catalogo = Catalogos.objects.filter(id=uid)
        if catalogo.count() == 0:
            raise Exception("No existe ningun registro con esa identificación")
        catalogo.delete()
        return RemoveDataCatalogo(success="ok")
