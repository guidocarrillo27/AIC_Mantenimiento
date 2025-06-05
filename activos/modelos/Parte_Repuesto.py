from django.db import models
from .Parte import Parte
from .Repuesto import Repuesto

class ParteRepuesto(models.Model):

    parte=models.ForeignKey(Parte,on_delete=models.CASCADE) 
    repuesto=models.ForeignKey(Repuesto,on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
 
    def __str__(self):
        return f"{self.parte.nombre} - {self.repuesto.nombre} ({self.cantidad})"

