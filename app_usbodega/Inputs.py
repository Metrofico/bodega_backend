import graphene


class InputRegisterUser(graphene.InputObjectType):
    nombre = graphene.String(required=True)
    apellido = graphene.String(required=True)
    email = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class InputLoginUser(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
