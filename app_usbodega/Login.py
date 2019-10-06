import graphene
from django.core.exceptions import ObjectDoesNotExist

from app_usbodega.models import *
from . import Inputs


class Login(graphene.AbstractType):
    user = graphene.Field(UsuarioType, login=Inputs.InputLoginUser())

    def resolve_user(self, info, login):
        try:
            usuario = Usuario.objects.get(email=login.email, password=login.password)
            usuario.password = ""
        except ObjectDoesNotExist:
            raise Exception("El usuario no existe")
        return usuario
