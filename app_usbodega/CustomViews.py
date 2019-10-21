from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_file_upload.django import FileUploadGraphQLView


class SentryGraphQLView(FileUploadGraphQLView):

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() != "post":
            raise Exception("Exception Invalid")
        cookies = request.COOKIES
        setattr(request, 'cookies', cookies)
        result = super().dispatch(request, *args, **kwargs)
        if result.status_code == 200:
            try:
                response_cookies = getattr(request, "middleware_cookies")
                for cookie in response_cookies:
                    result.set_cookie(cookie.get('key'), cookie.get('value'), max_age=31449600,
                                      httponly=cookie.get('httpOnly', False), secure=cookie.get('secure', False),
                                      samesite=cookie.get('SameSite', None))
            except:
                pass

        return result

    def execute_graphql_request(self, *args, **kwargs):
        if self.request.method.lower() != "post":
            raise Exception("Exception")
        result = super().execute_graphql_request(*args, **kwargs)
        return result
