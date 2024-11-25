from tkinter.constants import CASCADE

from django.contrib.auth.hashers import make_password
from django.db import models
from core.encryption_helper import EncryptionHelper


# modelo y sus especificaciones
class Users(models.Model):
    name = models.TextField()
    fecha_de_incripcion = models.DateField(auto_now_add=True)
    fecha_inicio_contrato = models.DateField()
    fecha_final_contrato = models.DateField()
    activo = models.BooleanField(default=True)
    id_plan_servicio = models.IntegerField()
    nombre_empresa = models.TextField()
    password = models.TextField()
    correo = models.TextField()
    telefono = models.TextField()
    id_sucursal_dafault = models.IntegerField()

    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'users' #nombre de la tabla en mi bd

    def __str__(self):
        return self.name
    #encirptar telefono

    #guardar
    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
                self.password = make_password(self.password)

            # Encriptar teléfono al guardar


        super().save(*args, **kwargs)

#modelo de sucursaes
class Sucursal(models.Model):
    nombre = models.TextField()
    direccion = models.TextField()
    telefono = models.TextField() #encripar
    id_usuario = models.IntegerField() #foreykey
    id_encargado = models.IntegerField()

    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'sucursal'


    def __str__(self):
        return self.nombre

    def get_telefono_decrypted(self):
        if self.telefono:
            encryption_helper = EncryptionHelper()
            return encryption_helper.decrypt_data(self.telefono)
        return None
        # guardar

    def save(self, *args, **kwargs):
        if self._state.adding:
            # Encriptar teléfono al guardar
            encryption_helper = EncryptionHelper()
            self.telefono = encryption_helper.encrypt_data(self.telefono)

        super().save(*args, **kwargs)


class Permisos_plan(models.Model):
    id_plan = models.IntegerField()
    id_modulo = models.IntegerField()
    tiene_permiso = models.CharField()

    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'permisos_plan'


    def __str__(self):
        return self.tiene_permiso


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

