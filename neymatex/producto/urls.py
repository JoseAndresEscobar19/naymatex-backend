from django.urls import path
from .views import *
from .apps import ProductoConfig

app_name = ProductoConfig.name
urlpatterns = [
    path('', ListarProductos.as_view(), name='listar'),
    path('agregar/', CrearProducto.as_view(), name='agregar'),
    path('editar/<pk>/', EditarProducto.as_view(), name='editar'),
    path('eliminar/<pk>/', producto_confirmar_eliminacion,
         name='eliminar'),
    path('activar/<pk>/', producto_confirmar_activar,
         name='activar'),
]
