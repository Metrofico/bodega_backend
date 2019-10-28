import graphene


class InputRegisterUser(graphene.InputObjectType):
    nombres = graphene.String(required=True)
    apellidos = graphene.String(required=True)
    correo = graphene.String(required=True)
    usuario = graphene.String(required=True)
    clave = graphene.String(required=True)


class AddProvedor(graphene.InputObjectType):
    ruc = graphene.String(required=True)
    razonsocial = graphene.String(required=True)
    direccion = graphene.String(required=True)
    telefono = graphene.String(required=True)


class InputAddProducto(graphene.InputObjectType):
    descripcion = graphene.String(required=True)
    umedida = graphene.String(required=True)
    presentacion = graphene.String(required=True)
    categorias = graphene.String(required=True)
    subcategoria = graphene.String(required=True)


class InputAddUnidadMedida(graphene.InputObjectType):
    descripcion = graphene.String(required=True)
    abreviatura = graphene.String(required=True)


class InputAddPresentacionArticulos(graphene.InputObjectType):
    descripcion = graphene.String(required=True)


class InputAddCategorias(graphene.InputObjectType):
    codigo = graphene.String(required=True)
    nombre = graphene.String(required=True)


class InputAddSubCategorias(graphene.InputObjectType):
    descripcion = graphene.String(required=True)
    categoria = graphene.String(required=True)


class InputLoginUser(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)
