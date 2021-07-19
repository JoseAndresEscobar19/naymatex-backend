from django.urls import path
from .views import *
from .apps import NotificacionConfig

app_name = NotificacionConfig.name
urlpatterns = [
    path('', ListarNotificaciones.as_view(), name='listar'),
    path('enviar/', CrearNotificacion.as_view(), name='agregar',),
    path('reenviar/<pk>/', notificacion_reenviar,
         name='reenviar'),
]
