import graphene


class UsuarioType(graphene.ObjectType):
    nombre = graphene.String()
    apellido = graphene.String()
    email = graphene.String()
    usuario = graphene.String()


class NotificacionType(graphene.ObjectType):
    bt_class = graphene.String()
    title = graphene.String()
    date = graphene.String()
    content = graphene.String()
