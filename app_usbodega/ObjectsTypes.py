import graphene


class UsuarioType(graphene.ObjectType):
    nombres = graphene.String()
    apellidos = graphene.String()
    usuario = graphene.String()
    email = graphene.String()
    token = graphene.String()


class NotificacionType(graphene.ObjectType):
    bt_class = graphene.String()
    title = graphene.String()
    date = graphene.String()
    content = graphene.String()
