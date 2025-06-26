from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from activos.modelos.Area import Area
from activos.modelos.SubArea import SubArea
from activos.modelos.Maquina import Maquina
from activos.modelos.mantenimientos import mantenimientos
from activos.modelos.Parte import Parte
from activos.modelos.Parte_Repuesto import ParteRepuesto
from activos.modelos.Repuesto import Repuesto
from activos.modelos.Categoria import Categoria
from .forms import CrearNuevaTarea, CrearNuevaArea, CrearMantenimiento,VerMantenimiento,VerMaquina,DetalleMantenimiento,NuevaMaquina,ActualizaMaquina,NuevaParte,ActualizaParte,VerParte,RepuestoForm,CategoriaForm, ParteRepuestoForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib.auth.decorators import login_required

# Vistas generales
def index(request):
    title='Programa de Mantenimiento'
    return render(request,'index.html', {'titulo':title})

def about(request):
    username='guido'
    return render(request,'about.html',{
        'usuario':username
    })

def hello(request,username):
    print(username)
    i=1
    return HttpResponse("<h1>Hola %s tu codigo es %s</h1>"%username %i)

#Vista para User and login
def logearse (request):
    if (request.method == 'GET'):
        return render(request,'logeo.html',{
            'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(username=request.POST['username'],
                                    password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('index')              
            except IntegrityError: 
                return render(request,'logeo.html',{
                    'form':UserCreationForm,
                    'error':'Username already exist'
                    })  
           
        return render(request,'logeo.html',{
                    'form':UserCreationForm,
                    'error':'Contraseñas son incorrectas'
                    })  
           
def salir(request):
    logout(request)
    return redirect('index')

def entrar(request):
    if request.method=='GET':
        return  render(request,'signin.html',{
       'form':AuthenticationForm 
        })
    else:
        print(request.POST)
        user=authenticate(request,username=request.POST['username'],
                      password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form':AuthenticationForm, 
                'error':'Usuario o password incorrecto'
                })
        else:
            login(request,user)
            return redirect('areas')
 
#Vista para crear locaciones y areas
def areas(request):
    #areas=list(Area.objects.values())
    #return JsonResponse(areas,safe=False)
    areas=Area.objects.all()
    return render(request,'areas/areas.html',{
        'locaciones':areas
    })

def subAreas(request):
    #sa=SubArea.objects.get(id=id)
    #return HttpResponse('Subarea: %s'%sa.nombre)
    sa=SubArea.objects.all()
    return render(request,'subareas/subareas.html',{
        'subareas':sa
    })

def crear_area(request):
    if request.method=='GET':
        return render(request,'areas/crear_area.html',{'form':CrearNuevaArea()})
    else:
        Area.objects.create(cod_area=request.POST['codigo'],
            nombre=request.POST['nombre'])
        return redirect('areas')

def detalle_areas(request,id):
    area=get_object_or_404(Area,id=id)
    subareas=SubArea.objects.filter(subarea_id=id)
    return render(request,'areas/detalle_areas.html',{
        'area':area,
        'subareas':subareas
    })

def detalle_subareas(request,id):
    subarea=get_object_or_404(SubArea,id=id)
    maquinas=Maquina.objects.filter(area_id=id)
    return render(request,'subareas/detalle_subareas.html',{
        'subarea':subarea,
        'maquinas':maquinas
    })

def crear_subarea(request):
    #print(request.GET['codigo'])
    #print(request.GET['nombre'])

    if request.method == 'GET':
        #voy a mostrar la interface
        return render(request,'subareas/crear_subarea.html',{'form':CrearNuevaTarea()})
    else:
        #print(request.POST)
        SubArea.objects.create(subarea_id=request.POST['subarea'],
                               nombre=request.POST['nombre'],
                            cod_subArea=request.POST['cod_subArea'])
        return redirect('detalle_areas',id=request.POST['subarea'])

#Vista para maquinas
@login_required
def nueva_maquina(request,id):   
    cant_maquina=Maquina.objects.filter(area_id=id).count()
    maquina=Maquina.objects.filter(area_id=id)

    lista=[]
    for p in maquina:
        lista.append(p.num_maquina)
    print(lista)
    item=1

    while item <= cant_maquina:
        if item in lista:
            item +=1
        else:
            break
    print(item)

    if request.method=='GET':
        area=get_object_or_404(SubArea,pk=id)
        print(NuevaMaquina())
        return render(request,'subareas/nueva_maquina.html',{
        'area':area,
        'form':NuevaMaquina()})
    else:
        area=get_object_or_404(SubArea,pk=id)
        form=NuevaMaquina(request.POST,request.FILES)
        if form.is_valid():
            nueva_maquina=form.save(commit=False)
            nueva_maquina.area_id=area.id
            nueva_maquina.num_maquina=item
            nueva_maquina.codigo=area.cod_subArea+'-M'+str(item)
            nueva_maquina.save()      
            return redirect('detalle_subareas',id=id)
        else:
            print(form.errors)
        
        return render(request,'subareas/nueva_maquina.html',{
        'form':NuevaMaquina()})

def actualiza_maquina(request,id):
    if request.method=='GET':
        maquina=get_object_or_404(Maquina,id=id)
        form=ActualizaMaquina(instance=maquina)
        activa_guarda=True
        return render(request,'maquinas/actualiza_maquina.html',{
        'maquina':maquina,
        'activa_guarda':activa_guarda,
        'form1':form})
    else:
        try:
            maquina=get_object_or_404(Maquina,pk=id)
            form=ActualizaMaquina(request.POST,request.FILES,instance=maquina)
            form.save()
            #return redirect('/subareas/1')
            #return redirect('detalle_subareas',id=maquina.area_id)
            return redirect('detalle_maquina',id=maquina.id)
        except ValueError:
            return render(request,'maquinas/detalle_maquina.html',{
                                'maquina':maquina,
                                'activa_guarda':activa_guarda,
                                'error':"Error actualizando la maquina",
                                'form1':form})
 
def ListarMaquinas(request):
    #return HttpResponse('Máquinas')
    maquinas=Maquina.objects.all()
    return render(request,'maquinas/maquinas.html',{
        'maquinas':maquinas
    })

def detalle_maquina(request,id):
    maquina=get_object_or_404(Maquina,id=id)
    form=VerMaquina(instance=maquina)
    activa_guarda=False

    partes=Parte.objects.filter(maquina_id=id)
    return render(request,'maquinas/detalle_maquina.html',{
        'maquina':maquina,
        'activa_guarda':activa_guarda,
        'form':form,
        'partes':partes
    })

#Vista para partes
@login_required
def nueva_parte(request,id):
    cant_parte=Parte.objects.filter(maquina_id=id).count()
    parte=Parte.objects.filter(maquina_id=id)

    lista=[]
    for p in parte:
        lista.append(p.num_parte)
    print(lista)

    item=1
    while item <= cant_parte:
        if item in lista:
            item +=1
        else:
            break
    print(item)

    if request.method=='GET':
        maquina=get_object_or_404(Maquina,pk=id)

        return render(request,'partes/nueva_parte.html',{
        'maquina':maquina,
        'form':NuevaParte()})
    else:
        maquina=get_object_or_404(Maquina,pk=id)
        form=NuevaParte(request.POST,request.FILES)
        if form.is_valid():
            nueva_parte=form.save(commit=False)
            nueva_parte.maquina_id=maquina.id
            nueva_parte.num_parte=item
            nueva_parte.codigo_parte=maquina.codigo+'-P'+str(item)
            nueva_parte.save()
            return redirect('detalle_maquina',id=id)
        else:
            print(form.errors)
        
        return render(request,'partes/nueva_parte.html',{
        'form':()})

def detalle_parte(request,id):
    parte=get_object_or_404(Parte,id=id)
    parte_repuestos=ParteRepuesto.objects.filter(parte=parte)

    #obtener todos los repuestos disponibles
    repuestos=Repuesto.objects.all()

    #crea un formulario para agregar un nuevo repuesto
    if request.method == 'POST':
        form=ParteRepuestoForm(request.POST)
        if form.is_valid():
            parte_seleccionada=parte
            repuesto_seleccionado=form.cleaned_data['repuesto']
            cantidad_seleccionada=form.cleaned_data['cantidad']

            #crear una nueva relación Parte-Repuesto
            ParteRepuesto.objects.create(parte=parte_seleccionada, repuesto=repuesto_seleccionado, cantidad=cantidad_seleccionada)
            return redirect('detalle_parte',id=parte.id)
    else:
        form=ParteRepuestoForm(initial={'parte':parte})
    
    #form2=VerParte(instance=parte)
    return render(request,'partes/detalle_parte.html',{
        'parte':parte,
        'parte_repuestos':parte_repuestos,
        'form':form,
        'repuestos':repuestos,
        
    })

@login_required        
def actualiza_parte(request,id):
    if request.method=='GET':
        parte=get_object_or_404(Parte,pk=id)
        print(parte)
        form=ActualizaParte(instance=parte)
        activa_guarda=True
        return render(request,'partes/actualiza_parte.html',{
        'parte':parte,
        'activa_guarda':activa_guarda,
        'form1':form})
    else:
        try:
            parte=get_object_or_404(Parte,pk=id)
            form=ActualizaParte(request.POST,request.FILES,instance=parte)
            form.save()
            #return redirect('/subareas/1')
            return redirect('detalle_maquina',id=parte.maquina_id)
        except ValueError:
            return render(request,'partes/actualiza_parte.html',{
                                'parte':parte,
                                'activa_guarda':activa_guarda,
                                'error':"Error actualizando la maquina",
                                'form1':form})

def eliminar_parte(request, pk):
    parte = get_object_or_404(Parte, pk=pk)
    if request.method == 'POST':
        parte.delete()
        return redirect('detalle_maquina',id=parte.maquina_id)
    return render(request, 'confirmar_eliminacion.html', {'objeto': parte})

#Vista para mantenimientos      
def crear_mantenimiento(request,id):
    if request.method=='GET':
        maquina=get_object_or_404(Maquina,pk=id)
        return render(request,'mantenimientos/crear_mantenimiento.html',{
        'maquina':maquina,
        'form':CrearMantenimiento()})
    else:
        maquina=get_object_or_404(Maquina,pk=id)
        form=CrearMantenimiento(request.POST,request.FILES)
        if form.is_valid():
            nuevo_mantenimiento=form.save(commit=False)
            nuevo_mantenimiento.maquina_id=maquina.id
            nuevo_mantenimiento.user=request.user
            nuevo_mantenimiento.save()
            return redirect(f'/mantenimientos_pendiente/{id}')
        else:
            print(form.errors)
        
        return render(request,'mantenimientos/crear_mantenimiento.html',{
        'form':CrearMantenimiento()})

def detalle_mantenimiento(request,id):
        if request.method == 'GET':
            mantenimiento=get_object_or_404(mantenimientos,pk=id)
            form=DetalleMantenimiento(instance=mantenimiento)
            return render(request,'mantenimientos/detalle_mantenimiento.html',{
            'mantenimiento':mantenimiento,
            'form':form})
        else:
            try:
                mantenimiento=get_object_or_404(mantenimientos,pk=id)
                form=DetalleMantenimiento(request.POST,request.FILES,instance=mantenimiento)
                form.save()
                return redirect('mantenimiento_maquina_pendiente',id=mantenimiento.maquina_id)
            except ValueError:
                return render(request,'mantenimientos/detalle_mantenimiento.html',{
                            'mantenimiento':mantenimiento,
                            'error':"Error actualizando la actividad de mantenimiento",
                            'form':form})

def completa_mantenimiento(request,id):
    mantenimiento=get_object_or_404(mantenimientos,pk=id)
    if request.method=='POST':
        mantenimiento.fecha_ejecutada=timezone.now()
        mantenimiento.save()
        return redirect('mantenimiento_maquina_pendiente',id=mantenimiento.maquina_id)
    
def borra_mantenimiento(request,id):
    mantenimiento=get_object_or_404(mantenimientos,pk=id)
    if request.method=='POST':
        mantenimiento.delete()
        return redirect('mantenimiento_maquina_pendiente',id=mantenimiento.maquina_id)

def ver_mantenimiento(request,id):
    if request.method == 'GET':
        #mantenimiento=mantenimientos.objects.get(pk=id)
        mantenimiento=get_object_or_404(mantenimientos,pk=id)
        form=VerMantenimiento(instance=mantenimiento)
        return render(request,'mantenimientos/ver_mantenimiento.html',{
            'mantenimiento':mantenimiento,
            'form':form})
   
def MantenimientoMaquinas_pendiente(request,id):
    #return HttpResponse('Máquinas')
    maquina=get_object_or_404(Maquina,id=id)
    detalle_mantenimiento=mantenimientos.objects.filter(maquina_id=id,fecha_ejecutada__isnull=True).order_by('-fecha_ejecutada')

    return render(request,'mantenimientos/mantenimiento_maquina.html',{
            'maquina':maquina,'mantenimientos':detalle_mantenimiento})

def MantenimientoMaquinas_completo(request,id):
    
    maquina=get_object_or_404(Maquina,id=id)
    detalle_mantenimiento=mantenimientos.objects.filter(maquina_id=id,fecha_ejecutada__isnull=False).order_by('-fecha_ejecutada')

    return render(request,'mantenimientos/mantenimiento_maquina.html',{
            'maquina':maquina,'mantenimientos':detalle_mantenimiento})

#Vista para repuestos
def crear_repuesto(request):
    categorias=Categoria.objects.all()
    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_repuestos')
    else:
        form = RepuestoForm()
    return render(request, 'repuestos/crear_repuesto.html', {'form': form, 'categorias':categorias})

def actualizar_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == 'POST':
        form = RepuestoForm(request.POST, request.FILES, instance=repuesto)
        if form.is_valid():
            form.save()
            return redirect('lista_repuestos')
    else:
        form = RepuestoForm(instance=repuesto)
    return render(request, 'repuestos/crear_repuesto.html', {'form': form})

def eliminar_repuesto(request, pk):
    repuesto = get_object_or_404(Repuesto, pk=pk)
    if request.method == 'POST':
        repuesto.delete()
        return redirect('lista_repuestos')
    return render(request, 'repuestos/confirmar_eliminacion.html', {'objeto': repuesto})

def lista_repuestos(request):
    categorias = Categoria.objects.all()  

    # Obtener los parámetros de búsqueda y filtro de los parámetros GET
    categoria_id = request.GET.get('categoria', None)
    if categoria_id:
        try:
            categoria_id=int(categoria_id)
        except ValueError:
            categoria_id=None

    busqueda = request.GET.get('busqueda', '')
    
    if categoria_id:
        repuestos = Repuesto.objects.filter(categoria_id=categoria_id)  # Filtrar por categoría
    else:
        repuestos = Repuesto.objects.all()  # Si no hay filtro, mostrar todos los repuestos
    
    if busqueda:
        repuestos = repuestos.filter(nombre__istartswith=busqueda)  # Filtrar por las primeras letras del nombre

 # Paginación de los repuestos
    paginator = Paginator(repuestos, 10)  # Mostrar 10 repuestos por página
    page_number = request.GET.get('page')  # Obtener el número de página de los parámetros GET
    page_obj = paginator.get_page(page_number)

    return render(request, 'repuestos/lista_repuestos.html', {
        'categorias': categorias,
        'repuestos': page_obj,
        'busqueda': busqueda,
        'categoria_id': categoria_id,
    })

def detalle_repuesto(request, id):
    repuesto=get_object_or_404(Repuesto, pk=id)

    form=RepuestoForm(instance=repuesto)
    return render(request,'repuestos/detalle_repuesto.html',{
        'repuesto':repuesto,
        'form':form,
    })

def buscar_repuestos(request):
    # Obtener el término de búsqueda desde el parámetro GET
    query = request.GET.get('term', '')
    
    # Filtrar los repuestos que coincidan con el término de búsqueda
    repuestos = Repuesto.objects.filter(nombre__icontains=query)  # búsqueda insensible a mayúsculas y minúsculas
    
    # Devolver los nombres de los repuestos como una lista de JSON
    results = []
    for repuesto in repuestos:
        results.append({'id': repuesto.id, 'label': repuesto.nombre})  # Cada elemento debe tener 'id' y 'label'
    
    return JsonResponse(results, safe=False)

def eliminar_parte_repuesto(request,id):
    parte_repuesto=get_object_or_404(ParteRepuesto,id=id)

    if request.method=='POST':
        print(parte_repuesto)
        parte_repuesto.delete()
        return redirect('detalle_parte',id=parte_repuesto.parte.id)
    return HttpResponse('Método no permitido',status=405)

#Vista para categorias
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('crear_repuesto')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear_categoria.html', {'form': form})

def actualizar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'crear_categoria.html', {'form': form})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('lista_categorias')
    return render(request, 'confirmar_eliminacion.html', {'objeto': categoria})

def lista_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias/lista_categorias.html', {'categorias': categorias})
