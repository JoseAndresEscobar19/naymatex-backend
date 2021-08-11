import django_filters
from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from django_filters.widgets import RangeWidget
from neymatex.models import *
from neymatex.orden.forms import OrdenFilterForm


class OrdenFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    empleado = django_filters.ModelChoiceFilter(
        queryset=Empleado.objects.filter(usuario__groups__name="Ventas"))
    cajero = django_filters.ModelChoiceFilter(
        queryset=Empleado.objects.filter(usuario__groups__name="Caja"))
    despachador = django_filters.ModelChoiceFilter(
        queryset=Empleado.objects.filter(usuario__groups__name="Despacho"))

    class Meta:
        model = Orden
        fields = ["created_at",
                  "estado",
                  'empleado',
                  'cajero',
                  'despachador',
                  ]
        form = OrdenFilterForm
