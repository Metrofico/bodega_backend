import graphene


class User(graphene.ObjectType):
    userName = graphene.String()


class Mutation(graphene.AbstractType):
    register = User

    def resolve_register(self, info, **kwargs):
        return User(userName="holas")

    pass


class Query(graphene.AbstractType):
    user = graphene.String()
