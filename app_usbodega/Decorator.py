from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_django.views import GraphQLView


class SentryGraphQLView(GraphQLView):

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() == "get":
            raise Exception("Exception Invalid")
        result = super().dispatch(request, *args, **kwargs)
        return result

    def execute_graphql_request(self, *args, **kwargs):
        if self.request.method.lower() == "get":
            raise Exception("Exception")
        result = super().execute_graphql_request(*args, **kwargs)

        return result
