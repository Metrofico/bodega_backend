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
            usuario = Usuario.objects.get(email=login.email)
            passwordu = login.password.encode("utf-8")
            print("Usuario: ", passwordu, " ", " bd: ", usuario.password.encode("utf-8"))
            if not bcrypt.checkpw(passwordu, usuario.password.encode("utf-8")):
                raise Exception("Identificacion incorrecta")
        except ObjectDoesNotExist:
            raise Exception("El usuario no existe")
        return ObjectsTypes.UsuarioType(nombre=usuario.nombre, apellido=usuario.apellido, email=usuario.email)
