from email.policy import default

import graphene
from graphene_django import DjangoObjectType
from sqlalchemy import select
from sqlalchemy.testing.suite.test_reflection import users
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from django.core.signing import Signer
from sawa_admin.apps import SawaAdminConfig
from sawa_admin.models import Users, Sucursal


class EncryptionHelper:
    def __init__(self):
        # Asegúrate de tener esta KEY en settings.py
        # settings.ENCRYPTION_KEY = Fernet.generate_key()
        self.cipher_suite = Fernet(settings.ENCRYPTION_KEY)
        self.signer = Signer()

    def encrypt_data(self, data):
        if not data:
            return None
        return self.cipher_suite.encrypt(str(data).encode()).decode()

    def decrypt_data(self, encrypted_data):
        if not encrypted_data:
            return None
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()

#se crear un modelo especificando el tipo de datos que graphql puede consultar

class UserType(DjangoObjectType):
    class Meta:
        model = Users
        fields = ("id", "name", "fecha_de_incripcion", "fecha_inicio_contrato", "fecha_final_contrato",
                  "activo", "id_plan_servicio", "nombre_empresa", "correo", "password", "telefono", "id_sucursal_dafault")

class SucursalType(DjangoObjectType):
    class Meta:
        model = Sucursal
        fields = ("id", "nombre", "direccion", "telefono", "id_usuario", "id_encargado")

 # Hacer el campo nullable en GraphQL
    idEncargado = graphene.Int(required=False)

class CreateUserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        fecha_inicio_contrato = graphene.Date()
        fecha_final_contrato = graphene.Date()
        nombre_empresa = graphene.String()
        id_plan_servicio = graphene.Int()
        correo = graphene.String()
        password = graphene.String()
        telefono = graphene.String()

    user = graphene.Field(UserType)  #esto es lo que retorna

    def mutate(self, info, name, fecha_inicio_contrato, fecha_final_contrato,
               nombre_empresa, id_plan_servicio, password, correo, telefono):


        newUser = Users(name = name, fecha_inicio_contrato = fecha_inicio_contrato,
              fecha_final_contrato = fecha_final_contrato, nombre_empresa = nombre_empresa,
              id_plan_servicio = id_plan_servicio, correo = correo,
              telefono = telefono, password = password )
        newUser.save()
        return CreateUserMutation(user = newUser)

class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        activo = graphene.Boolean()
    user = graphene.Field(UserType)

    def mutate(self, info, id, activo):
        user = Users.objects.get(pk=id)
        user.activo = activo
        user.save()
        return UpdateUserMutation(user = user)
#urls
class Query(graphene.ObjectType):
    hello = graphene.String(default_value = "Hi!")
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.String())
    sucursales = graphene.List(SucursalType)

    def resolve_users(self, info):
        return Users.objects.all()

    def resolve_user(self, info, id):
        return Users.objects.get(pk=id)

    def resolve_sucursales(self, info):
        return Sucursal.objects.all()

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
