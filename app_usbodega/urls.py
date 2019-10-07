from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from app_usbodega import controller
from app_usbodega.Decorator import SentryGraphQLView

urlpatterns = [
    url('csrf/', controller.csrf),
    url(r'^gql', csrf_exempt(SentryGraphQLView.as_view(graphiql=False, batch=True)))
]
