from django.db import models

class Permisos_plan(models.Model):
    id_plan = models.IntegerField()
    id_modulo = models.IntegerField()
    tiene_permiso = models.CharField()

    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'permisos_plan'


    def __str__(self):
        return self.tiene_permiso