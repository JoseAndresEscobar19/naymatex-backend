from django.urls import path, include
from .views import *
from .apps import NeymatexConfig

app_name = NeymatexConfig.name

urlpatterns = [
    path('', home, name="principal"),
    path('ajax-filtro-ventas', dashboard_filter_ventas, name='dashboard_ventas'),
    path('ajax-filtro-recaudacion', dashboard_filter_recaudacion,
         name='dashboard_recaudacion'),
    path('ajax-filtro-productos', dashboard_productos_mas_vendidos,
         name='dashboard_productos'),
    # Clientes
    path('clientes/', include('neymatex.cliente.urls', namespace="cliente")),
    # Producto
    path('producto/', include('neymatex.producto.urls', namespace="producto")),
    # Ordenes
    path('orden/', include('neymatex.orden.urls', namespace="orden")),
    # Notificaciones
    path('notificacion/', include('neymatex.notificacion.urls',
         namespace="notificacion")),
]
