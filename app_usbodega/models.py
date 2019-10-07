from django.db import models


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=1024)
