from django.urls import path
from . import views
urlpatterns=[
    path('',views.index),
    path('agregarUsuario/',views.agregarUsuario),
    path('listadoUsuarios/',views.listadoUsuarios),
    path('guardarUsuario/',views.guardarUsuario),
    path('eliminarUsuario/<id_usuario>',views.eliminarUsuario),

    path('agregarEvento/',views.agregarEvento),
    path('listadoEventos/',views.listadoEventos),
    path('guardarEvento/',views.guardarEvento),
    path('editarEvento/<id_evento>',views.editarEvento),
    path('procesarEdicionEvento/',views.procesarEdicionEvento),

    path('agregarParticipacion/',views.agregarParticipacion),
     path('listadoParticipacion/',views.listadoParticipacion),
     path('guardarParticipacion/',views.guardarParticipacion),
     path('listar_notificaciones/', views.listar_notificaciones),
]