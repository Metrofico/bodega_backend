import graphene
from django.db import IntegrityError

from . import Inputs
from .models import UsuarioType, Usuario


class Register(graphene.Mutation):
    class Arguments:
        registerinput = Inputs.InputRegisterUser(required=True)

    user = graphene.Field(UsuarioType)

    def mutate(self, info, registerinput):
        user = Usuario(nombre=registerinput.nombre, apellido=registerinput.apellido, email=registerinput.email,
                       password=registerinput.password)
        try:
            user.save()
        except IntegrityError:
            raise Exception("La cuenta ya existe")
        return Register(user=user)
