import graphene


class UsuarioType(graphene.ObjectType):
    nombres = graphene.String()
    apellidos = graphene.String()
    usuario = graphene.String()
    email = graphene.String()
    token = graphene.String()


class CatalogoType(graphene.ObjectType):
    payload = graphene.String()


class CatalogoList(graphene.ObjectType):
    id = graphene.String()
    nombre = graphene.String()
    file = graphene.String()
    subida = graphene.String()


class CatalogoUpdateCurrent(graphene.ObjectType):
    success = graphene.String()


class CatalogoClearCurrent(graphene.ObjectType):
    success = graphene.String()


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


class CurrentCatalogoObj(graphene.ObjectType):
    id_existencia = graphene.String()
    descripcion = graphene.String()
    item_presupuestario = graphene.String()
