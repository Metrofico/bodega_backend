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


class AreasType(graphene.ObjectType):
    id = graphene.Int()
    area = graphene.String()


class CargosType(graphene.ObjectType):
    id = graphene.Int()
    cargo = graphene.String()


class BeneficiarioType(graphene.ObjectType):
    id = graphene.Int()
    tipo_doc = graphene.String()
    documento = graphene.String()
    nombres = graphene.String()
    apellido_paterno = graphene.String()
    apellido_materno = graphene.String()
    area = graphene.String()
    cargo = graphene.String()
    fecha_registro = graphene.String()
    fecha_modificacion = graphene.String()
    telefono = graphene.String()
