# from django.contrib import admin
from django.conf.urls import url
from django.urls import include
from graphene_django.views import GraphQLView

urlpatterns = [
    url('api/', include('app_usbodega.urls')),
    url(r'^graphiql', GraphQLView.as_view(batch=False, graphiql=True)),
    #    path('admin/', admin.site.urls),
]
