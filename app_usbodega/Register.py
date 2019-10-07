import bcrypt
import graphene
from django.db import IntegrityError

from . import Inputs
from .ObjectsTypes import UsuarioType
from .models import Usuarios


class Register(graphene.Mutation):
    class Arguments:
        registerinput = Inputs.InputRegisterUser(required=True)

    user = graphene.Field(UsuarioType)

    def mutate(self, info, registerinput):

        passwordu = registerinput.password.encode("utf-8")
        try:
            hashed_password = bcrypt.hashpw(passwordu, bcrypt.gensalt())
        except Exception:
            raise Exception("Invalid Error")
        user = Usuarios(nombre=registerinput.nombre, apellido=registerinput.apellido, email=registerinput.email,
                       password=str(hashed_password, "utf-8"))
        try:
            user.save()
        except IntegrityError:
            raise Exception("La cuenta ya existe")
        return Register(user=UsuarioType(nombre=user.nombre, apellido=user.apellido, email=user.email))
