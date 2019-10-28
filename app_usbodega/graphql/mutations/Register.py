import uuid

import bcrypt
import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from app_usbodega import filters
from app_usbodega.graphql import Inputs
from app_usbodega.graphql.objetos.ObjectsTypes import UsuarioType
from app_usbodega.models import Usuarios


def cleanstr(i):
    return str(i).strip()


class Logout(graphene.Mutation):
    result = graphene.Boolean()

    def mutate(self, info):
        cookies = getattr(info.context, 'cookies', None)
        regenerate = str(uuid.uuid4()).replace("-", "") + str(uuid.uuid4()).replace("-", "")
        if cookies is not None and "oAtmp" in cookies:
            setattr(info.context, "middleware_cookies", [
                {
                    'key': "oAtmp",
                    'value': regenerate,
                    'httpOnly': True,
                    'secure': False,
                }
            ])
            return Logout(result=True)
        return Logout(result=False)


class AddProducto(graphene.Mutation):
    class Arguments:
        addproducto = Inputs.InputAddProducto(required=True)

    descripcion = graphene.String()

    def mutate(self, info, addproducto):
        descripcion = addproducto.descripcion
        return AddProducto(descripcion=descripcion)


class Register(graphene.Mutation):
    class Arguments:
        registerinput = Inputs.InputRegisterUser(required=True)

    user = graphene.Field(UsuarioType)

    def mutate(self, info, registerinput):
        clave = registerinput.clave
        username = registerinput.usuario
        filters.strfilters(str=clave, min_length=8, errormessageminlength="La clave debe ser mayor o igual a $length")
        filters.strfilters(str=username, min_length=5,
                           errormessageminlength="El usuario debe ser mayor o igual a $length")
        passwordu = registerinput.clave.encode("utf-8")
        try:
            hashed_password = bcrypt.hashpw(passwordu, bcrypt.gensalt())
        except Exception:
            raise Exception("Error al procesar su contraseña, intente nuevamente")

        try:
            Usuarios.objects.get(usuario=username)
            raise Exception("Error el nombre de usuario ya existe")
        except ObjectDoesNotExist:
            try:
                Usuarios.objects.get(email=registerinput.correo)
                raise Exception("Error el correo electronico ya existe")
            except ObjectDoesNotExist:
                user = Usuarios(nombres=cleanstr(registerinput.nombres), apellidos=cleanstr(registerinput.apellidos),
                                usuario=cleanstr(registerinput.usuario),
                                email=cleanstr(registerinput.correo),
                                password=str(hashed_password, "utf-8"))
                try:
                    user.save()
                except IntegrityError:
                    raise Exception("Error de integridad al registrarse")
                return Register(
                    user=UsuarioType(nombres=user.nombres, usuario=user.usuario, apellidos=user.apellidos,
                                     email=user.email))
