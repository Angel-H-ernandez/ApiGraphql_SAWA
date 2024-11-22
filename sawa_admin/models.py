from django.contrib.auth.hashers import make_password
from django.db import models
from core.encryption_helper import EncryptionHelper


# Create your models here.
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
        db_table = 'users'


    def __str__(self):
        return self.name

    def get_telefono_decrypted(self):
        if self.telefono:
            encryption_helper = EncryptionHelper()
            return encryption_helper.decrypt_data(self.telefono)
        return None

    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
                self.password = make_password(self.password)

            # Encriptar teléfono al guardar
            encryption_helper = EncryptionHelper()
            self.telefono = encryption_helper.encrypt_data(self.telefono)

        super().save(*args, **kwargs)


class Sucursal(models.Model):
    nombre = models.TextField()
    direccion = models.TextField()
    telefono = models.TextField()
    id_usuario = models.BigIntegerField()
    id_encargado = models.BigIntegerField()

    class Meta:
        managed = False  # No gestionar las migraciones de este modelo
        db_table = 'sucursal'


    def __str__(self):
        return self.name