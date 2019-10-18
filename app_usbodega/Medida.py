import graphene

from app_usbodega.Inputs import InputAddUnidadMedida


class Medida(graphene.Mutation):
    class Arguments:
        addmedida = InputAddUnidadMedida(required=True)

    descripcion = graphene.String()

    def mutate(self, info, addmedida):
        return Medida(descripcion=addmedida.descripcion)
