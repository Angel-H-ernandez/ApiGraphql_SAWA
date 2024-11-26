from django.contrib.auth.hashers import make_password
from django.db import models

class User(models.Model):
    nombre = models.TextField()
    fecha_inscripcion = models.DateField(auto_now_add=True)
    fecha_inicio_contrato = models.DateField()
    fecha_final_contrato = models.DateField()
    activo = models.BooleanField(default=True)
    id_plan_servicio = models.IntegerField()
    nombre_empresa = models.TextField()
    password = models.TextField()
    correo = models.TextField()
    telefono = models.TextField()


    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'users' #nombre de la tabla en mi bd

    def __str__(self):
        return self.nombre
    #encirptar telefono

    #guardar
    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
                self.password = make_password(self.password)

            # Encriptar teléfono al guardar


        super().save(*args, **kwargs)