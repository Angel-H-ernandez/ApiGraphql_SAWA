from email.policy import default
import graphene
from core.mutationss.permiso_plan_mutation import PermisosPlanType, CreatePermisosPlanMutation, \
    UpdatePermisosPlanMutation
from core.mutationss.plan_servicio_mutations import PlanServicioType, CreatePlanServicioMutation, \
    UpdatePlanServicioMutation
from core.mutationss.sucursal_mutations import SucursalType, CreateSucursalMutation, UpdateSucursalMutation
from core.mutationss.user_mutations import UserType, CreateUserMutation, UpdateUserMutation
from sawa_admin.models import User, Sucursal, Permisos_plan, Plan_servicio

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
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

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
