import graphene


class InputRegisterUser(graphene.InputObjectType):
    nombres = graphene.String(required=True)
    apellidos = graphene.String(required=True)
    correo = graphene.String(required=True)
    usuario = graphene.String(required=True)
    clave = graphene.String(required=True)


class InputAddProducto(graphene.InputObjectType):
    ruc = graphene.String(required=True)
    razonsocial = graphene.String(required=True)


class InputLoginUser(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)