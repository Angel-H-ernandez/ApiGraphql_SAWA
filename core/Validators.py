import re
from django.core.exceptions import ValidationError

def validar_correo(correo):
    patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(patron_correo, correo):
        raise ValidationError("El correo electrónico no tiene un formato válido.")

def validar_telefono(telefono):
    patron_telefono = r'^\+?[1-9]\d{9}$'
    if not re.match(patron_telefono, telefono):
        raise ValidationError("El número de teléfono no tiene un formato válido.")
