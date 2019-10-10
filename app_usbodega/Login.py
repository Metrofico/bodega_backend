import datetime

import bcrypt
import graphene
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from app_usbodega.models import *
from . import Inputs
from . import ObjectsTypes


class Login(graphene.AbstractType):
    user = graphene.Field(ObjectsTypes.UsuarioType, login=Inputs.InputLoginUser())
    get_notifications = graphene.List(ObjectsTypes.NotificacionType)

    def resolve_user(self, info, login):

        try:
            usuario = Usuarios.objects.get(username=login.username)
            passwordu = login.password.encode("utf-8")
            try:
                if not bcrypt.checkpw(passwordu, usuario.password.encode("utf-8")):
                    raise Exception("La clave ingresada es incorrecta")
            except Exception:
                raise Exception("La clave ingresada es incorrecta")
        except ObjectDoesNotExist:
            raise Exception("El usuario que escribio no existe")

        expiry = str(datetime.date.today() + datetime.timedelta(days=2))
        payload = {
            'id': usuario.id,
            'exp': expiry
        }
        token = str(jwt.encode(payload, str(settings.SECRET_KEY_JWT)), "utf8")
        setattr(info.context, "middleware_cookies", [
            {
                'key': "oAtmp",
                'value': token,
                'httpOnly': True,
                'secure': False,
            }
        ])
        return ObjectsTypes.UsuarioType(nombres=usuario.nombres, usuario=usuario.username,
                                        apellidos=usuario.apellidos,
                                        email=usuario.email, token=token)

    def resolve_get_notifications(self, info):
        data = Notificaciones.objects.all().filter(actived=True)
        retorno = []
        for item in data:
            bt_class = item.bt_cl.lower()
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

            retorno.append(ObjectsTypes.NotificacionType(bt_class=style_class, title=item.title, date=item.date,
                                                         content=item.content))

        return retorno
