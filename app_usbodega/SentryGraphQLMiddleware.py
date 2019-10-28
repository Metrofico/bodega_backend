from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_file_upload.django import FileUploadGraphQLView

from app_usbodega import utils
from app_usbodega.graphql import secure_graphql


class SentryGraphQLView(FileUploadGraphQLView):

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        if self.graphiql is False:
            if request.method.lower() != "post":
                raise Exception("Exception Invalid")
        cookies = request.COOKIES
        setattr(request, 'cookies', cookies)
        if cookies is not None and "oAtmp" in cookies:
            token = cookies.get('oAtmp')
            decoded = utils.logindecode(token)
            if decoded:
                setattr(request, "auth", decoded)
        result = super().dispatch(request, *args, **kwargs)
        if result.status_code == 200:
            try:
                response_cookies = getattr(request, "middleware_cookies")
                for cookie in response_cookies:
                    result.set_cookie(cookie.get('key'), cookie.get('value'), max_age=31449600,
                                      httponly=cookie.get('httpOnly', False), secure=cookie.get('secure', False),
                                      samesite=cookie.get('SameSite', None))
            except (ValueError, Exception):
                return result

        return result

    def execute_graphql_request(self, *args, **kwargs):
        if self.graphiql is False:
            if self.request.method.lower() != "post":
                raise Exception("Exception")
        # OPERATION NAME
        if self.graphiql is False:
            graphql = args[1]
            secure_graphql.validar_sesion_operacion(graphql, settings.GRAPHQL_EXCEPT_QUERIES)
        result = super().execute_graphql_request(*args, **kwargs)
        return result
