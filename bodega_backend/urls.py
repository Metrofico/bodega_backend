# from django.contrib import admin
import channels
from django.conf.urls import url
from django.urls import include
from app_usbodega.downloads_requests import download
from .schema import MyGraphqlWsConsumer

urlpatterns = [
    url('api/', include('app_usbodega.urls')),
    url('api/downloads', download)
]

websocket_urlpatterns = [
    url(r'^graphql', MyGraphqlWsConsumer),
]

application = channels.routing.ProtocolTypeRouter(
    {
        "websocket": channels.routing.URLRouter(websocket_urlpatterns)
    }
)
