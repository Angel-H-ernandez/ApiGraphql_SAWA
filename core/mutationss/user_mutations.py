import graphene
from django.contrib.auth.hashers import make_password
from graphene_django import DjangoObjectType
from sawa_admin.models import User
from core.Validators import validar_telefono, validar_correo



class UserType(DjangoObjectType):
    # Campo para obtener el teléfono desencriptado
    telefono_decrypted = graphene.String()
    class Meta:
        model = User
        fields = ("id", "nombre", "fecha_inscripcion", "fecha_inicio_contrato", "fecha_final_contrato",
                  "activo", "id_plan_servicio", "nombre_empresa", "correo", "password", "telefono")

    nombreEmpresa = graphene.String(required=False)  # Permite valores nulos
    fecha_inscripcion = graphene.String(required=False)  # Permite valores nulos
    fecha_inicio_contrato = graphene.String(required=False)
    fecha_final_contrato = graphene.String(required=False)
    correo = graphene.String(required=False)
    password = graphene.String(required=False)
    telefono = graphene.String(required=False)



    def resolve_telefono_decrypted(self, info):
        """Retorna el teléfono desencriptado"""
        return self.get_telefono_decrypted()

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        fecha_inicio_contrato = graphene.Date(required=True)
        fecha_final_contrato = graphene.Date(required=True)
        nombre_empresa = graphene.String(required=True)
        id_plan_servicio = graphene.Int(required=True)
        correo = graphene.String(required=True)
        password = graphene.String(required=True)
        telefono = graphene.String(required=True)

    user = graphene.Field(UserType)  #esto es lo que retorna

    def mutate(self, info, nombre, fecha_inicio_contrato, fecha_final_contrato,
               nombre_empresa, id_plan_servicio, password, correo, telefono):

        validar_correo(correo)
        validar_telefono(telefono)

        newUser = User(nombre = nombre, fecha_inicio_contrato = fecha_inicio_contrato,
              fecha_final_contrato = fecha_final_contrato, nombre_empresa = nombre_empresa,
              id_plan_servicio = id_plan_servicio, correo = correo,
              telefono = telefono, password = password )
        newUser.save()
        return CreateUserMutation(user = newUser)

class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        activo = graphene.Boolean()
        telefono = graphene.String(required=False)
        nombre_empresa = graphene.String(required=False)
        correo = graphene.String(required=False)
        password = graphene.String(required=False)
        fecha_inicio_contrato = graphene.Date(required=False)
        fecha_final_contrato = graphene.Date(required=False)

    user = graphene.Field(UserType)

    """def mutate(self, info, id, activo = None, telefono = None, nombre_empresa = None, correo = None, password = None,
               fecha_inicio_contrato = None, fecha_final_contrato = None):

        user = User.objects.get(pk=id)
        if activo is not None:
            user.activo = activo
        if telefono is not None:
            user.telefono = telefono
        if nombre_empresa is not None:
            user.nombre_empresa = nombre_empresa
        if correo is not None:
            user.correo = correo
        if password is not None:
            user.password = make_password(password)
        if fecha_inicio_contrato is not None:
            user.fecha_inicio_contrato = fecha_inicio_contrato
        if fecha_final_contrato is not None:
            user.fecha_final_contrato = fecha_final_contrato


        user.save()
        return UpdateUserMutation(user = user)"""

    def mutate(self, info, id, **kwargs):
        user = User.objects.get(pk=id)
        for key, value in kwargs.items():
            if value is not None:
                setattr(user, key, value)

        if kwargs.get("password"):
            user.password = make_password(kwargs["password"])

        user.save()
        return UpdateUserMutation(user=user)