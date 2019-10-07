import graphene


class UsuarioType(graphene.ObjectType):
    nombre = graphene.String()
    apellido = graphene.String()
    email = graphene.String()
    usuario = graphene.String()
