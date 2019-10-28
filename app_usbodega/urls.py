from django.conf.urls import url

from app_usbodega.SentryGraphQLMiddleware import SentryGraphQLView

urlpatterns = [
    url(r'^gql', SentryGraphQLView.as_view(graphiql=True, batch=False))
]
