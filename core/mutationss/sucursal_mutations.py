import graphene
from graphene_django import DjangoObjectType
from sawa_admin.models import Sucursal
from core.Validators import validar_telefono


class SucursalType(DjangoObjectType):
    class Meta:
        model = Sucursal
        fields = ("id", "nombre", "direccion", "telefono", "id_usuario")

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
