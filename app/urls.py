from django.urls import path

from app import controller

urlpatterns = [
    path('', controller.init)
]