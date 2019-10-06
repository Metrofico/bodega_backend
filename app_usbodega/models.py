from django.db import models
from graphene_django import DjangoObjectType


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=1024)


class UsuarioType(DjangoObjectType):
    class Meta:
        model = Usuario
