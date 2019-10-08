import graphene


class UsuarioType(graphene.ObjectType):
    nombre = graphene.String()
    apellido = graphene.String()
    username = graphene.String()
    email = graphene.String()
    token = graphene.String()


class NotificacionType(graphene.ObjectType):
    bt_class = graphene.String()
    title = graphene.String()
    date = graphene.String()
    content = graphene.String()
