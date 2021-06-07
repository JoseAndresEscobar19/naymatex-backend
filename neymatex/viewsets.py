from rest_framework import permissions, viewsets

from .models import *
from .serializers import *

# API.


class ClienteView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()


class EmpleadoView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EmpleadoSerializer
    queryset = Empleado.objects.all()


class TipoCategoriaView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = TipoCategoriaSerializer
    queryset = TipoCategoria.objects.all()


class CategoriaView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()


class ProductoView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()
