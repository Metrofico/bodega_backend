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

    def resolve_get_notifications(self, info):
        data = notificaciones.objects.all().filter(actived=True)
        retorno = []
        for item in data:
            bt_class = item.bt_cl.lower()
            style_class = str
            if bt_class == "success":
                style_class = "bg-success"
            elif bt_class == "danger":
                style_class = "bg-danger"
            elif bt_class == "warning":
                style_class = "bg-warning"
            elif bt_class == "info":
                style_class = "bg-info"
            else:
                style_class = "bg-secondary"
            print(style_class)
            retorno.append(ObjectsTypes.NotificacionType(bt_class=style_class, title=item.title, date=item.date,
                                                         content=item.content))

        return retorno
