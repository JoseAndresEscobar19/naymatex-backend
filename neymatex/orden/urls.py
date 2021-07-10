from django.urls import path
from .views import *
from .apps import OrdenConfig

app_name = OrdenConfig.name
urlpatterns = [
    path('', ListarOrdenes.as_view(), name='listar'),
    # path('agregar/', CrearOrden.as_view(), name='agregar'),
    # path('editar/<pk>/', EditarOrden.as_view(), name='editar'),
    path('eliminar/<pk>/', orden_confirmar_eliminacion,
         name='eliminar')
]
