import graphene
from graphene_django import DjangoObjectType
from sawa_admin.models import Permisos_plan


class PermisosPlanType(DjangoObjectType):
    class Meta:
        model = Permisos_plan
        fields = ("id", "id_plan", "id_modulo", "tiene_permiso")

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