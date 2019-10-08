import bcrypt
import graphene
from django.db import IntegrityError

from . import Inputs
from .ObjectsTypes import UsuarioType
from .models import Usuarios


def cleanstr(i):
    return str(i).strip()


class Register(graphene.Mutation):
    class Arguments:
        registerinput = Inputs.InputRegisterUser(required=True)

    user = graphene.Field(UsuarioType)

    def mutate(self, info, registerinput):

        passwordu = registerinput.password.encode("utf-8")
        try:
            hashed_password = bcrypt.hashpw(passwordu, bcrypt.gensalt())
        except Exception:
            raise Exception("La clave ingresada es incorrecta")
        user = Usuarios(nombres=cleanstr(registerinput.nombre), apellidos=cleanstr(registerinput.apellido),
                        username=cleanstr(registerinput.username),
                        email=cleanstr(registerinput.email),
                        password=str(hashed_password, "utf-8"))
        try:
            user.save()
        except IntegrityError:
            raise Exception("La cuenta ya existe")
        return Register(user=UsuarioType(nombre=user.nombres, apellido=user.apellidos, email=user.email))
