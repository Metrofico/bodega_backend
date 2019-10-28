# from django.contrib import admin
import channels
from django.conf.urls import url
from django.urls import include

from .schema import MyGraphqlWsConsumer

urlpatterns = [
    url('api/', include('app_usbodega.urls')),
]

websocket_urlpatterns = [
    url(r'^graphql', MyGraphqlWsConsumer),
]

application = channels.routing.ProtocolTypeRouter(
    {
        "websocket": channels.routing.URLRouter(websocket_urlpatterns)
    }
)
