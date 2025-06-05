from django import forms
from django.forms import ModelForm,SelectDateWidget
from activos.modelos.Area import Area
from activos.modelos.SubArea import SubArea
from activos.modelos.Maquina import Maquina
from activos.modelos.mantenimientos import mantenimientos
from activos.modelos.Parte import Parte
from activos.modelos.Parte_Repuesto import ParteRepuesto
from activos.modelos.Repuesto import Repuesto
from activos.modelos.Categoria import Categoria
from django.contrib.admin import widgets 

class CrearNuevaTarea(ModelForm):
    #codigo=forms.CharField(label='Código')  #es para crear input tipo texto
    #nombre=forms.CharField(label='Nombre subárea',widget=forms.Textarea)

    class Meta:
        model=SubArea 
        fields=['subarea','nombre','cod_subArea']
    
        widgets={
            'cod_subArea':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese código area'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre area'})
        }

class CrearNuevaArea(forms.Form):
    nombre=forms.CharField(label='Nombre área',widget=forms.Textarea)
    codigo=forms.CharField(label='Código')  #es para crear input tipo texto    

class NuevaMaquina(ModelForm):
    class Meta:
        model=Maquina
        fields=['nombre','descripcion','disponibilidad','fecha_instalacion','foto','link']

        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre máquina'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de máquina'}),
            'fecha_instalacion':forms.widgets.DateInput(attrs={'type':'date'})                                
        }

class NuevaParte(ModelForm):
    class Meta:
        model=Parte
        fields=['nombre','descripcion','mantenimiento','foto','anexo']

        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre parte'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'}),
            'mantenimiento':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'})                              
        }

class CrearMantenimiento(ModelForm):
    #fecha_planificada=forms.DateField(widget = forms.SelectDateWidget())

    class Meta:
        model=mantenimientos
        fields=['tipo','nombre','descripcion','fecha_planificada','responsable']

        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre actividad'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7'}),
            'fecha_planificada':forms.widgets.DateInput(attrs={'type':'date'})
        }

class DetalleMantenimiento(ModelForm):
    class Meta:
        model=mantenimientos
        fields=['tipo','nombre','descripcion','fecha_planificada','responsable','evidencia']
        
        widgets={
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Ingrese nombre actividad'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7'}),
            'fecha_planificada':forms.widgets.DateInput(attrs={'type':'date'})
        }
        
class VerMantenimiento(ModelForm):
    class Meta:
        model=mantenimientos
        fields="__all__"    #se usa para ver todos los campos

class VerMaquina(ModelForm):
    class Meta:
        model=Maquina
        fields="__all__"    #se usa para ver todos los campos

        fields=['area','codigo','descripcion',
                'disponibilidad','fecha_instalacion','link']

        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control',
                                                'rows':'5'})                                                
        }

class ActualizaMaquina(ModelForm):
    class Meta:
        model=Maquina
        fields="__all__"    #se usa para ver todos los campos

        widgets={
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre máquina'}),
            'fecha_instalacion':forms.widgets.DateInput(attrs={'type':'date'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control',
                                                'rows':'5'})                                                
        }

class VerParte(ModelForm):
    class Meta:
        model=Parte
        fields="__all__"    #se usa para ver todos los campos

        widgets={
            'codigo_parte':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese código parte'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre parte'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'}),
            'mantenimiento':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'})                              
        }

class ActualizaParte(ModelForm):
    class Meta:
        model=Parte
        fields="__all__"    #se usa para ver todos los campos

        widgets={
            'codigo_parte':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese código parte'}),
            'nombre':forms.TextInput(attrs={'class':'form-control',
                                            'placeholder':'Ingrese nombre parte'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'}),
            'mantenimiento':forms.Textarea(attrs={'class':'form-control','rows':'7',
                                            'placeholder':'Ingrese descripcion de parte'})                              
        }

class CategoriaForm(ModelForm):
    class Meta:
        model=Categoria
        fields=['nombre']

class RepuestoForm(ModelForm):
    class Meta:
        model = Repuesto
        fields = ['categoria', 'nombre', 'descripcion', 'cantidad_bodega', 'foto', 'anexo']

class ParteRepuestoForm(ModelForm):
    class Meta:
        model = ParteRepuesto
        fields = ['repuesto', 'cantidad']




