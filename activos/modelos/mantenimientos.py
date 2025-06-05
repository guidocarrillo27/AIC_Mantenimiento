from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError
from uuid import uuid4
from .Maquina import Maquina

class mantenimientos(models.Model):

    def nombrar(instance,filename):
        ext = filename.split('.')[-1].lower()
        
        if instance.pk:
            filename = '{}.{}'.format(instance.nombre, ext)
        else:
            # set filename as random string
            filename = ''.join(['content', instance.user.username, filename])
        # return the whole path to the file
        return os.path.join("mantenimientos_maquinas", filename)  
    
    tipo_servicio = [
        ("PRE","PREVENTIVO"),
        ("CORR","CORRECTIVO"),
        ("DIC","PREDICTIVO")
    ]

    maquina=models.ForeignKey(Maquina,on_delete=models.CASCADE)
    tipo=models.CharField(max_length=5,choices=tipo_servicio)
    nombre=models.CharField(max_length=200)  
    descripcion=models.TextField()
    fecha_planificada=models.DateField()
    fecha_ejecutada=models.DateField(null=True,blank=True)
    responsable=models.ForeignKey(User,on_delete=models.CASCADE)
    evidencia=models.FileField(upload_to=nombrar,null=True,blank=True)

    def __str__(self):
        return str(self.maquina.nombre) +' - '+self.nombre






