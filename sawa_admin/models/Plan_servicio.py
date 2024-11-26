from django.db import models

class Plan_servicio(models.Model):
    nombre = models.CharField()
    precio = models.IntegerField()
    periodo = models.CharField()
    activo = models.BooleanField()

    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'plan_servicio'


    def __str__(self):
        return self.nombre
