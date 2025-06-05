from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),                            #cuando visita la ruta principal, voy a ejecutar la función hello
    path('about/',views.about,name="about"),   
    path('login/',views.logearse,name="logearse"),    
    path('logout/',views.salir,name="logout"),      
    path('signin/',views.entrar,name="signin"),         
    path('areas/',views.areas,name="areas"),
    path('areas/<int:id>',views.detalle_areas,name="detalle_areas"),
    path('subareas/',views.subAreas,name="subareas"),
    path('subareas/<int:id>',views.detalle_subareas,name="detalle_subareas"),
    path('crear_subarea/',views.crear_subarea,name="crear_subarea"),
    path('crear_area/',views.crear_area,name="crear_area"),

    #Referente a las máquinas
    path('maquinas/',views.ListarMaquinas,name="maquinas"),
    path('maquinas/<int:id>',views.detalle_maquina,name="detalle_maquina"),
    path('maquinas/<int:id>/actualiza',views.actualiza_maquina,name="actualiza_maquina"),
    path('subareas/crea/<int:id>',views.nueva_maquina,name="nueva_maquina"),

    #Referente a las partes
    path('parte/<int:id>',views.detalle_parte,name="detalle_parte"),
    path('parte/crea/<int:id>',views.nueva_parte,name="nueva_parte"),
    path('parte/act/<int:id>',views.actualiza_parte,name="actualiza_parte"),

    #Referente a los mantenimientos
    path('mantenimiento/<int:id>/crea',views.crear_mantenimiento,name="crear_mantenimiento"),
    path('mantenimiento/<int:id>/ver',views.ver_mantenimiento,name="ver_mantenimiento"),
    path('mantenimiento/<int:id>/detalle',views.detalle_mantenimiento,name="detalle_mantenimiento"),
    path('mantenimiento/<int:id>/completa',views.completa_mantenimiento,name="completa_mantenimiento"),
    path('mantenimiento/<int:id>/borra',views.borra_mantenimiento,name="borra_mantenimiento"),
    path('mantenimientos_pendiente/<int:id>',views.MantenimientoMaquinas_pendiente,name="mantenimiento_maquina_pendiente"),
    path('mantenimientos_completo/<int:id>',views.MantenimientoMaquinas_completo,name="mantenimiento_maquina_completo"),

    #Referente a los repuestos y categorías
    path('crear_repuesto/',views.crear_repuesto,name="crear_repuesto"),
    path('repuestos/',views.lista_repuestos,name="lista_repuestos"),
    path('buscar-repuestos/',views.buscar_repuestos,name="buscar_repuestos"),
    path('crear_categoria/',views.crear_categoria,name="crear_categoria"),
    path('eliminar-parte-repuesto/<int:id>/',views.eliminar_parte_repuesto,name="eliminar_parte_repuesto"),
]