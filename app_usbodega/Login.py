import bcrypt
import graphene
from django.core.exceptions import ObjectDoesNotExist

from app_usbodega.models import *
from . import Inputs
from . import ObjectsTypes


class Login(graphene.AbstractType):
    user = graphene.Field(ObjectsTypes.UsuarioType, login=Inputs.InputLoginUser())

    def resolve_user(self, info, login):
        try:
            usuario = Usuarios.objects.get(email=login.email)
            passwordu = login.password.encode("utf-8")
            try:
                if not bcrypt.checkpw(passwordu, usuario.password.encode("utf-8")):
                    raise Exception("La clave ingresada es incorrecta")
            except Exception:
                raise Exception("La clave ingresada es incorrecta")
        except ObjectDoesNotExist:
            raise Exception("El usuario que escribio no existe")
        return ObjectsTypes.UsuarioType(nombre=usuario.nombres, apellido=usuario.apellidos, email=usuario.email)
