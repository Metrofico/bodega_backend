import graphene


class Beneficiario(graphene.ObjectType):
    get_beneficiarios = graphene.String()

    def resolve_get_beneficiarios(self, info):
        pass

    pass
