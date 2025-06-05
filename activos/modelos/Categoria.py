from django.db import models
from django.core.exceptions import ValidationError 

class Categoria(models.Model):
    # Campos para el modelo Repuestos
    nombre = models.CharField(max_length=100, unique=True)

    def clean(self):
        # Validar que el nombre de la categoría no sea duplicado
        if Categoria.objects.filter(nombre=self.nombre).exists():
            raise ValidationError(f'Ya existe una categoría con el nombre "{self.nombre}".')

    def __str__(self):
        return self.nombre
    

