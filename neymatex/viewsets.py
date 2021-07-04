from django.db.models import Q
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get_queryset(self):
        query = self.request.query_params.get('q')
        queryset = Producto.objects.all()
        if query:
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(codigo__icontains=query))
        return queryset


class OrdenAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        return Response(Orden.objects.all())
