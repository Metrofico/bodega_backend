import graphene


class Mutation(graphene.AbstractType):
    register = graphene.String()


class Query(graphene.AbstractType):
    user = graphene.String()
