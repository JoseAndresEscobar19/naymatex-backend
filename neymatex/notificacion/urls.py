from django.urls import path
from .views import *
from .apps import NotificacionConfig

app_name = NotificacionConfig.name
urlpatterns = [
    path('', ListarNotificaciones.as_view(), name='listar'),
    path('enviar/', CrearNotificacion.as_view(), name='agregar',),
    # path('editar/<pk>/', EditarCliente.as_view(), name='editar'),
    path('eliminar/<pk>/', cliente_confirmar_eliminacion,
         name='eliminar'),
    path('activar/<pk>/', cliente_confirmar_activar,
         name='activar'),
]
