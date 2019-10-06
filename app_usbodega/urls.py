from django.urls import path

from app_usbodega import controller

urlpatterns = [
    path('', controller.init)
]