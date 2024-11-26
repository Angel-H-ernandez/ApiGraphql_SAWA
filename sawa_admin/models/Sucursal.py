
from django.db import models
from core.encryption_helper import EncryptionHelper

class Sucursal(models.Model):
    nombre = models.TextField()
    direccion = models.TextField()
    telefono = models.TextField() #encripar
    id_usuario = models.IntegerField() #foreykey


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