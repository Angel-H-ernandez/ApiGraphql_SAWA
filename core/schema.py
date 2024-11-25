from email.policy import default


import graphene
from django.core.exceptions import ValidationError
from graphene_django import DjangoObjectType
from sqlalchemy import select
from sqlalchemy.testing.suite.test_reflection import users
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from django.core.signing import Signer
from sawa_admin.apps import SawaAdminConfig
from sawa_admin.models import Users, Sucursal, Permisos_plan, Plan_servicio
import re


# Función para validar formato de correo
def validar_correo(correo):
    # Expresión regular para validar el correo electrónico
    patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(patron_correo, correo):
        raise ValidationError("El correo electrónico no tiene un formato válido.")

# Función para validar formato de teléfono (ejemplo)
def validar_telefono(telefono):
    # Expresión regular para validar el teléfono (puedes ajustarla según el formato requerido)
    patron_telefono = r'^\+?[1-9]\d{9}$'
    if not re.match(patron_telefono, telefono):
        raise ValidationError("El número de teléfono no tiene un formato válido.")

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
#types
class UserType(DjangoObjectType):
    # Campo para obtener el teléfono desencriptado
    telefono_decrypted = graphene.String()
    class Meta:
        model = Users
        fields = ("id", "name", "fecha_de_incripcion", "fecha_inicio_contrato", "fecha_final_contrato",
                  "activo", "id_plan_servicio", "nombre_empresa", "correo", "password", "telefono", "id_sucursal_dafault")

    nombreEmpresa = graphene.String(required=False)  # Permite valores nulos
    fecha_de_incripcion = graphene.String(required=False)  # Permite valores nulos
    fecha_inicio_contrato = graphene.String(required=False)
    fecha_final_contrato = graphene.String(required=False)
    correo = graphene.String(required=False)
    password = graphene.String(required=False)
    telefono = graphene.String(required=False)
    id_sucursal_dafault = graphene.String(required=False)


    def resolve_telefono_decrypted(self, info):
        """Retorna el teléfono desencriptado"""
        return self.get_telefono_decrypted()

class SucursalType(DjangoObjectType):
    class Meta:
        model = Sucursal
        fields = ("id", "nombre", "direccion", "telefono", "id_usuario", "id_encargado")

 # Hacer el campo nullable en GraphQL
    idEncargado = graphene.Int(required=False)

class PermisosPlanType(DjangoObjectType):
    class Meta:
        model = Permisos_plan
        fields = ("id", "id_plan", "id_modulo", "tiene_permiso")

class PlanServicioType(DjangoObjectType):
    class Meta:
        model = Plan_servicio
        fields = ("id", "nombre", "precio", "periodo", "activo")
# crear
class CreateUserMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        fecha_inicio_contrato = graphene.Date(required=True)
        fecha_final_contrato = graphene.Date(required=True)
        nombre_empresa = graphene.String(required=True)
        id_plan_servicio = graphene.Int(required=True)
        correo = graphene.String(required=True)
        password = graphene.String(required=True)
        telefono = graphene.String(required=True)

    user = graphene.Field(UserType)  #esto es lo que retorna

    def mutate(self, info, name, fecha_inicio_contrato, fecha_final_contrato,
               nombre_empresa, id_plan_servicio, password, correo, telefono):

        validar_correo(correo)
        validar_telefono(telefono)

        newUser = Users(name = name, fecha_inicio_contrato = fecha_inicio_contrato,
              fecha_final_contrato = fecha_final_contrato, nombre_empresa = nombre_empresa,
              id_plan_servicio = id_plan_servicio, correo = correo,
              telefono = telefono, password = password )
        newUser.save()
        return CreateUserMutation(user = newUser)

class CreateSucursalMutation(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        direccion = graphene.String(required=False)
        telefono = graphene.String(required=False)
        id_usuario = graphene.String(required=True)
        id_encargado= graphene.Int(required=False)

    sucursal = graphene.Field(SucursalType)  # esto es lo que retorna

    def mutate(self, info, nombre, telefono, direccion,
               id_usuario, id_encargado):

        validar_telefono(telefono)

        newSucursal = Sucursal(nombre=nombre, direccion=direccion,
                        telefono=telefono, id_usuario=id_usuario,
                        id_encargado=id_encargado)
        newSucursal.save()
        return CreateSucursalMutation(sucursal = newSucursal)

class CreatePermisosPlanMutation(graphene.Mutation):
    class Arguments:
        id_plan = graphene.Int(required = True)
        id_modulo = graphene.Int(required = True)
        tiene_permiso = graphene.Boolean(required= True)

    permisos_plan = graphene.Field(PermisosPlanType)

    def mutate(self, info, id_plan, id_modulo, tiene_permiso):
        newPermisosPlan = Permisos_plan(id_plan = id_plan, id_modulo = id_modulo, tiene_permiso = tiene_permiso)
        newPermisosPlan.save()
        return CreatePermisosPlanMutation(permisos_plan = newPermisosPlan)

class CreatePlanServicioMutation(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required = True)
        precio = graphene.Int(required = True)
        periodo = graphene.String(required = True)
        activo = graphene.Boolean(required = True)

    plan_servicio = graphene.Field(PlanServicioType)

    def mutate(self, infro, nombre, precio, periodo, activo):
        newPlanServicio = Plan_servicio(nombre = nombre, precio = precio, periodo = periodo, activo = activo)
        newPlanServicio.save()
        return CreatePlanServicioMutation(plan_servicio = newPlanServicio)
#actualizar
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

    def mutate(self, info, id, activo = None, telefono = None, nombre_empresa = None, correo = None, password = None,
               fecha_inicio_contrato = None, fecha_final_contrato = None):

        user = Users.objects.get(pk=id)
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
        return UpdateUserMutation(user = user)

class UpdateSucursalMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        telefono = graphene.String(required=False)
        nombre = graphene.String(required=False)
        direccion = graphene.String(required=False)


    sucursal = graphene.Field(SucursalType)

    def mutate(self, info, id, telefono = None, nombre = None, id_encargado = None, direccion = None):

        sucursal = Sucursal.objects.get(pk=id)
        if nombre is not None:
            sucursal.nombre = nombre
        if telefono is not None:
            sucursal.telefono = telefono
        if id_encargado is not None:
            sucursal.id_encargado = id_encargado
        if direccion is not None:
            sucursal.correo = direccion



        sucursal.save()
        return UpdateSucursalMutation(sucursal = sucursal)

class UpdatePermisosPlanMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        id_plan = graphene.Int(required = False)
        id_modulo = graphene.Int(required = False)
        tiene_permiso = graphene.Boolean(required = False)
    permisos_plan = graphene.Field(PermisosPlanType)

    def mutate(self, info, id,  id_plan = None, id_modulo = None, tiene_permiso = None):
        permisos_plan = Permisos_plan.objects.get(pk=id)
        if id_plan is not None:
            permisos_plan.id_plan = id_plan
        if id_modulo is not None:
            permisos_plan.id_modulo = id_modulo
        if tiene_permiso is not None:
            permisos_plan.tiene_permiso = tiene_permiso



        permisos_plan.save()
        return UpdatePermisosPlanMutation(permisos_plan=permisos_plan)

class UpdatePlanServicioMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String(required = False)
        precio = graphene.Int(required = False)
        periodo = graphene.String(required = False)
        activo = graphene.Boolean(required = False)
    plan_servicio = graphene.Field(PlanServicioType)

    def mutate(self, info, id, nombre = None, precio = None, periodo = None, activo = None):
        plan_servicio = Plan_servicio.objects.get(pk=id)
        if nombre is not None:
            plan_servicio.nombre = nombre
        if precio is not None:
            plan_servicio.precio = precio
        if periodo is not None:
            plan_servicio.periodo = periodo
        if activo is not None:
            plan_servicio.activo = activo

        plan_servicio.save()
        return UpdatePlanServicioMutation(plan_servicio=plan_servicio)

#urls
class Query(graphene.ObjectType):

    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.String())
    sucursales = graphene.List(SucursalType)
    sucursal = graphene.Field(SucursalType, id=graphene.String())
    permisos_planes = graphene.List(PermisosPlanType)
    permisos_plan = graphene.Field(PermisosPlanType, id=graphene.String())
    planes_servicios = graphene.List(PlanServicioType)
    plan_servicio = graphene.Field(PlanServicioType, id=graphene.String())

    def resolve_users(self, info):
        return Users.objects.all()

    def resolve_user(self, info, id):
        return Users.objects.get(pk=id)

    def resolve_sucursales(self, info):
       return Sucursal.objects.all()

    def resolve_sucursal(self, info, id):
        return Sucursal.objects.get(pk=id)

    def resolve_permisos_planes(self, info):
        return Permisos_plan.objects.all()

    def resolve_permisos_plan(self, info, id):
        return Permisos_plan.objects.get(pk = id)

    def resolve_planes_servicios(self, info):
        return Plan_servicio.objects.all()

    def resolve_plan_servicio(self, info, id):
        return Plan_servicio.objects.get(pk = id)

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    create_sucursal = CreateSucursalMutation.Field()
    update_sucursal = UpdateSucursalMutation.Field()
    create_permiso_plan = CreatePermisosPlanMutation.Field()
    update_permiso_plan = UpdatePermisosPlanMutation.Field()
    create_plan_servicio = CreatePlanServicioMutation.Field()
    update_plan_servicio = UpdatePlanServicioMutation.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
