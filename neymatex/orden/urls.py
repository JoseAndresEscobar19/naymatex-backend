from django.urls import path
from .views import *
from .apps import OrdenConfig

app_name = OrdenConfig.name
urlpatterns = [
    path('', ListarOrdenes.as_view(), name='listar'),
    path('ver/<pk>/', VerOrden.as_view(), name='ver'),
    path('editar/<pk>/', EditarOrden.as_view(), name='editar'),
    path('eliminar/<pk>/', orden_confirmar_eliminacion,
         name='eliminar'),
    path('pagar/<pk>/', orden_confirmar_pagar,
         name='pagar'),
    path('despachar/<pk>/', orden_confirmar_despachar,
         name='despachar'),
    path('observacion/<pk>/', orden_observacion, name='observacion'),
]
