from django.db import models
from .Area import Area

class SubArea(models.Model):
    subarea=models.ForeignKey(Area,on_delete=models.CASCADE)
    cod_subArea=models.CharField(max_length=15)
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return self.nombre
