from datetime import datetime, timedelta

import bcrypt
import graphene
import jwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from app_usbodega.models import *
from . import Inputs
from . import ObjectsTypes


def logindecode(token):
    if str(token).strip():
        try:
            user = jwt.decode(token, str(settings.SECRET_KEY_JWT))
            if 'id' in user:
                if is_valid_uuid(user.get("id")):
                    return user
        except:
            return {}
    return {}


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


class Login(graphene.AbstractType):
    user = graphene.Field(ObjectsTypes.UsuarioType, login=Inputs.InputLoginUser())
    get_notifications = graphene.List(ObjectsTypes.NotificacionType)

    def resolve_user(self, info, login):
        # current date and time
        now = datetime.today() + timedelta(seconds=10)
        timestamp = datetime.timestamp(now)
        cookies = getattr(info.context, 'cookies', None)
        if cookies is not None and "oAtmp" in cookies:
            token = cookies.get('oAtmp')
            decoded = logindecode(token=token)
            if decoded:
                try:
                    usuario = Usuarios.objects.get(uid=uuid.UUID(str(decoded.get("id"))))
                    payload = {
                        'id': str(usuario.uid),
                        'exp': timestamp
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
                    return ObjectsTypes.UsuarioType(nombres=usuario.nombres, usuario=usuario.usuario,
                                                    apellidos=usuario.apellidos,
                                                    email=usuario.email, token=token)
                except:
                    pass
        if not login.username.strip() and not login.password.strip():
            print("Finded username and password empty no allowed")
            return None
        try:
            usuario = Usuarios.objects.get(usuario=login.username)
            passwordu = login.password.encode("utf-8")
            try:
                if not bcrypt.checkpw(passwordu, usuario.password.encode("utf-8")):
                    raise Exception("La clave ingresada es incorrecta")
            except Exception:
                raise Exception("La clave ingresada es incorrecta")
        except ObjectDoesNotExist:
            raise Exception("El usuario que escribio no existe: " + login.username)

        payload = {
            'id': str(usuario.uid),
            'exp': timestamp
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
        return ObjectsTypes.UsuarioType(nombres=usuario.nombres, usuario=usuario.usuario,
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
