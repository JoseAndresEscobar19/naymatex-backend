from django.urls import path, include
from .views import *
from .apps import NeymatexConfig

app_name = NeymatexConfig.name

urlpatterns = [
    path('', home, name="principal"),
    # Clientes
    path('clientes/', include('neymatex.cliente.urls', namespace="cliente")),
    # Producto
    path('producto/', include('neymatex.producto.urls', namespace="producto")),
]
