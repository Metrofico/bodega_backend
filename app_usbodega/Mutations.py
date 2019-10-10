import graphene
import graphql_jwt

from .Register import Register


class Mutation(graphene.ObjectType):
    register = Register.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
