import uuid

import bcrypt
import graphene
from django.db import IntegrityError

from app_usbodega.utils.GeneralDataValidation import strfilters
from . import Inputs
from .ObjectsTypes import UsuarioType
from .models import Usuarios


def cleanstr(i):
    return str(i).strip()


class Logout(graphene.Mutation):
    result = graphene.Boolean()

    @staticmethod
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

    ruc = graphene.String()

    @staticmethod
    def mutate(self, info, addproducto):
        ruc = addproducto.ruc
        strfilters(str=ruc, max_length=13, min_length=13)
        return AddProducto(ruc=ruc)


class Register(graphene.Mutation):
    class Arguments:
        registerinput = Inputs.InputRegisterUser(required=True)

    user = graphene.Field(UsuarioType)

    @staticmethod
    def mutate(self, info, registerinput):

        passwordu = registerinput.clave.encode("utf-8")
        try:
            hashed_password = bcrypt.hashpw(passwordu, bcrypt.gensalt())
        except Exception:
            raise Exception("La clave ingresada es incorrecta")

        user = Usuarios(nombres=cleanstr(registerinput.nombres), apellidos=cleanstr(registerinput.apellidos),
                        usuario=cleanstr(registerinput.usuario),
                        email=cleanstr(registerinput.correo),
                        password=str(hashed_password, "utf-8"))
        print(user.apellidos, " ", user.usuario, " ", user.email)
        try:
            user.save()
        except IntegrityError as e:
            print(e)
            raise Exception("La cuenta ya existe")
        return Register(
            user=UsuarioType(nombres=user.nombres, usuario=user.usuario, apellidos=user.apellidos, email=user.email))
