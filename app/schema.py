import graphene


class Mutation(graphene.AbstractType):
    register = graphene.String()

    def resolve_register(self, info, **kwargs):
        return "registrado"

    pass


class Query(graphene.AbstractType):
    user = graphene.String()
