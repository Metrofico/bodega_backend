import uuid

import jwt
from django.conf import settings


def f_horas(t_horas):
    return "horas" if t_horas > 1 or t_horas == 0 else "hora"


def f_minutos(t_minutos):
    return "minutos" if t_minutos > 1 or t_minutos == 0 else "minuto"


def f_segundos(t_segundos):
    return "segundos" if t_segundos > 1 or t_segundos == 0 else "segundo"


def is_valid_uuid(val):
    try:
        return uuid.UUID(str(val))
    except ValueError:
        return None


def logindecode(token):
    if str(token).strip():
        try:
            user = jwt.decode(token, str(settings.SECRET_KEY_JWT))
            if 'id' in user:
                if is_valid_uuid(user.get("id")):
                    return user
        except (ValueError, Exception):
            return {}
    return {}


def segundos_a_formato(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int((segundos % 3600) % 60)
    return str(horas) + " " + f_horas(horas) + " " + (
        str(minutos) + " " + f_minutos(minutos) if minutos != 0 else "") + " " + (
               str(segundos) + " " + f_segundos(segundos) if segundos != 0 else "") if horas >= 1 else (
        str(minutos) + " " + f_minutos(minutos) + " " + (
            str(segundos) + " " + f_segundos(segundos) if segundos != 0 else "")
        if int(minutos) >= 1 else str(
            segundos) + " " + f_segundos(segundos)
    )


def get_cookies_from_header_str(headers):
    cookies_get = {}
    for h in headers:
        if h == "Cookie":
            value = headers["Cookie"]
            cookies = value.split(";")
            for cookie in cookies:
                cookie = cookie.strip().split("=")
                key = cookie[0]
                value = cookie[1]
                cookies_get[key] = value
    return cookies_get


def get_cookies_from_header(headers):
    cookies_get = {}
    for h in headers:
        key = str(h[0], "utf8")
        if key == "cookie":
            cookies = str(h[1], "utf8").split(";")
            for cookie in cookies:
                cookie = cookie.strip().split("=")
                key = cookie[0]
                value = cookie[1]
                cookies_get[key] = value
    return cookies_get


def get_cookies_from_line(line_cookies):
    cookies_get = {}
    cookies = line_cookies.split(";")
    for cookie in cookies:
        cookie = cookie.strip().split("=")
        key = cookie[0]
        value = cookie[1]
        cookies_get[key] = value
    return cookies_get
