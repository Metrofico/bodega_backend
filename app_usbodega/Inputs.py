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


class InputRegisterBeneficiario(graphene.InputObjectType):
    tipo_doc = graphene.Int(required=True)
    documento = graphene.String(required=True)
    nombres = graphene.String(required=True)
    apellido_paterno = graphene.String(required=True)
    apellido_materno = graphene.String(required=True)
    telefono = graphene.String(required=True)
    area = graphene.Int(required=True)
    cargo = graphene.Int(required=True)


class InputUpdateBeneficiario(graphene.InputObjectType):
    target = graphene.Int(required=True)
    tipo_doc = graphene.Int()
    documento = graphene.String()
    nombres = graphene.String()
    apellido_paterno = graphene.String()
    apellido_materno = graphene.String()
    telefono = graphene.String()
    area = graphene.Int()
    cargo = graphene.Int()


class InputBeneficiarioQuery(graphene.InputObjectType):
    qType = graphene.String(required=True)
    beneficiario = graphene.String()


class InputRegisterCargo(graphene.InputObjectType):
    cargo = graphene.String(required=True)


class InputUpdateCargo(graphene.InputObjectType):
    target = graphene.Int(required=True)
    cargo = graphene.String(required=True)


class InputDeleteCargo(graphene.InputObjectType):
    target = graphene.Int(required=True)
