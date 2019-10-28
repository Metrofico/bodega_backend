import uuid as uuid

from django.db import models


class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    nombres = models.CharField(max_length=200)
    apellidos = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    usuario = models.CharField(max_length=50, blank=True, unique=True)
    password = models.CharField(max_length=1024)


class Notificaciones(models.Model):
    id = models.AutoField(primary_key=True)
    bt_cl = models.TextField(max_length=255)
    title = models.TextField(max_length=255)
    date = models.TextField(max_length=255)
    content = models.TextField(max_length=255)
    actived = models.BooleanField()


class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.TextField(unique=True)
    categoria = models.TextField(unique=True)


class Catalogos(models.Model):
    id = models.AutoField(primary_key=True)
    nameFile = models.TextField(max_length=255)
    file = models.FilePathField()
    date_uploaded = models.IntegerField()


class CurrentCatalogo(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_de_existencia = models.TextField(max_length=255)
    descripcion = models.TextField(max_length=255)
    item_presupuestario = models.TextField(max_length=255)


class Areas(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.TextField(max_length=100)


class Cargos(models.Model):
    id = models.AutoField(primary_key=True)
    cargo = models.TextField(max_length=100)


class Beneficiario(models.Model):
    id = models.AutoField(primary_key=True)
    tipo_doc = models.TextField(max_length=100)
    documento = models.TextField(max_length=13)
    nombres = models.TextField(max_length=100)
    apellido_paterno = models.TextField(max_length=100)
    apellido_materno = models.TextField(max_length=10)
    area = models.ForeignKey(Areas, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargos, on_delete=models.CASCADE)
    telefono = models.TextField(max_length=100)
    fecha_registro = models.TextField(max_length=255)
    fecha_modificacion = models.TextField(max_length=255)
