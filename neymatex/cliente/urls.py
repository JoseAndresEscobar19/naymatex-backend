from django.urls import path
from .views import *
from .apps import ClienteConfig

app_name = ClienteConfig.name
urlpatterns = [
    path('', ListarClientes.as_view(), name='listar'),
    path('agregar/', CrearCliente.as_view(), name='agregar',),
    path('editar/<pk>/', EditarCliente.as_view(), name='editar'),
    path('eliminar/<pk>/', cliente_confirmar_eliminacion,
         name='eliminar'),
    path('activar/<pk>/', cliente_confirmar_activar,
         name='activar'),
]
