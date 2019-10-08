from django.db import models


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, blank=True, unique=True)
    password = models.CharField(max_length=1024)


class Notificaciones(models.Model):
    id = models.AutoField(primary_key=True)
    bt_cl = models.TextField(max_length=255)
    title = models.TextField(max_length=255)
    date = models.TextField(max_length=255)
    content = models.TextField(max_length=255)
    actived = models.BooleanField()
