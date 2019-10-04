import graphene

import app.schema


class Mutations(
    app.schema.Mutation,
    graphene.ObjectType,
):
    pass


class Queries(
    app.schema.Query,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)
