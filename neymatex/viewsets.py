import datetime

from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from django.db.models.base import Model
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
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
        query_cat = self.request.query_params.get('cat')
        query_top = self.request.query_params.get('top')
        query_top_ventas = self.request.query_params.get('top_ventas')
        query_top_recaudacion = self.request.query_params.get('top_dinero')

        queryset = Producto.objects.all()
        if query_top:
            return queryset.order_by("nombre")[:int(query_top)]
        if query_top_ventas:
            current_month = timezone.now().astimezone().month
            return queryset.filter(detalles__orden__created_at__month=current_month,
                                   detalles__orden__estado__in=[Orden.Status.PAID, Orden.Status.DES]).annotate(num_ventas=Count(
                                       'detalles')).order_by('-num_ventas', 'nombre')[:int(query_top_ventas)]
        elif query_top_recaudacion:
            current_month = timezone.now().astimezone().month
            return queryset.filter(detalles__orden__created_at__month=current_month,
                                   detalles__orden__estado__in=[Orden.Status.PAID, Orden.Status.DES]).annotate(dinero_ventas=Sum(
                                       'detalles__valor_total')).order_by('-dinero_ventas', 'nombre')[:int(query_top_recaudacion)]
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | Q(codigo__icontains=query) | Q(alias__icontains=query))
        if query_cat:
            queryset = queryset.filter(categoria__nombre__icontains=query_cat)
        return queryset


class OrdenView(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = OrdenSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'created_at': ['date__range']}

    def get_queryset(self):
        query_empleado = self.request.query_params.get('emp')
        query_cliente = self.request.query_params.get('cli')
        query_pag = self.request.query_params.get('estado')
        query_last = self.request.query_params.get('last')
        queryset = Orden.objects.all()

        if query_pag:
            if query_pag == '0':
                queryset = queryset.filter(estado=Orden.Status.NOPAG)
            elif query_pag == '1':
                queryset = queryset.filter(estado=Orden.Status.PAID)
            elif query_pag == '2':
                queryset = queryset.filter(estado=Orden.Status.DES)
            elif query_pag == '9':
                queryset = queryset.filter(estado=Orden.Status.CANCEL)
        if query_cliente:
            queryset = queryset.filter(cliente_referencial=query_cliente)
        if query_empleado and query_last:
            return queryset.filter(
                empleado=query_empleado, created_at__date=timezone.now().astimezone().date())
        elif query_empleado:
            queryset = queryset.filter(empleado=query_empleado)
        if query_last:
            queryset = queryset[:1]
        return queryset


class NotificacionView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = NotificacionSerializer

    def get_queryset(self):
        query_empleado = self.request.query_params.get('emp')
        if query_empleado:
            return Notificacion.objects.filter(usuarios__empleado=query_empleado)
        return Notificacion.objects.none()
