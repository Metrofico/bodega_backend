from django.http import HttpResponse

import manage
from app_usbodega import utils


def download(request):
    error = "Sin autorización [Authorization error]"
    if request.method != "GET":
        error = "Sin autorización [010101]"
    elif not ("workspace" in request.GET):
        error = "Sin autorización [workspace]"
    elif not ("filename" in request.GET):
        error = "Sin autorización [021010]"
    cookies = None
    if "HTTP_COOKIE" in request:
        httpcookies = request.META["HTTP_COOKIE"]
        cookies = utils.get_cookies_from_line(httpcookies)
    if "Cookie" in request.headers:
        cookies = utils.get_cookies_from_header_str(request.headers)
    if cookies is not None:
        if "oAtmp" in cookies:
            user = utils.logindecode(cookies["oAtmp"])
            if not user:
                httpres = HttpResponse("Sin autorización [Invalid authentication]")
                httpres["Access-Control-Allow-Credentials"] = True
                httpres["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept"
                return httpres
            print(cookies)
            name = request.GET["filename"]
            try:
                path = manage.db_bodega_file_path(name)
                reader = open(path, "rb")
            except(ValueError, Exception):
                return HttpResponse("Sin autorización [Not found]")

            file = reader.read()
            response = HttpResponse(file)
            response['Content-Disposition'] = f'attachment; filename={name}'
            return response
    httres = HttpResponse(error)
    httres["Access-Control-Allow-Credentials"] = True
    httres["Access-Control-Allow-Headers"] = "Origin, Content-Type, Accept"
    return httres
