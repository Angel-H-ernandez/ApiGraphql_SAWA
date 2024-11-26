import graphene
from graphene_django import DjangoObjectType
from sawa_admin.models import Plan_servicio


class PlanServicioType(DjangoObjectType):
    class Meta:
        model = Plan_servicio
        fields = ("id", "nombre", "precio", "periodo", "activo")

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