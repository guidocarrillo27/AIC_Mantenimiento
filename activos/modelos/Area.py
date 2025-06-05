from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):
    cod_area=models.CharField(max_length=15)
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return str(self.nombre)




