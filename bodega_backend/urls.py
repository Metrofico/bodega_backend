# from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('', include('app_usbodega.urls')),
    url(r'^graphiql', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^gql', csrf_exempt(GraphQLView.as_view(batch=True, graphiql=False))),
    #    path('admin/', admin.site.urls),
]
