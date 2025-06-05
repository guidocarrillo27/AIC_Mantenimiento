from django.contrib import admin
from activos.modelos.Area import Area
from activos.modelos.SubArea import SubArea
from activos.modelos.Maquina import Maquina
from activos.modelos.mantenimientos import mantenimientos
from activos.modelos.Parte import Parte
from activos.modelos.Parte_Repuesto import ParteRepuesto
from activos.modelos.Categoria import Categoria
from activos.modelos.Repuesto import Repuesto

# Register your models here.
admin.site.register(Area)
admin.site.register(SubArea)
admin.site.register(Maquina)
admin.site.register(mantenimientos)
admin.site.register(Parte)
admin.site.register(ParteRepuesto)
admin.site.register(Repuesto)
admin.site.register(Categoria)
