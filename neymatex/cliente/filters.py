import django_filters
from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from django_filters.widgets import RangeWidget
from neymatex.cliente.forms import ClienteFilterForm
from neymatex.models import *


class ClienteFilter(django_filters.FilterSet):
    orden_cantidad = django_filters.NumericRangeFilter(
        method="cantidad_ordenes", widget=RangeWidget(attrs={"type": "number", "min": "0"}))
    orden_monto = django_filters.RangeFilter(method="ordenes_monto", widget=RangeWidget(
        attrs={"type": "number", "step": "0.01", "min": "0"}))
    orden_fechas = django_filters.DateFromToRangeFilter(
        method="ordenes_fechas", widget=RangeWidget(attrs={"type": "date"}))
    monto_credito = django_filters.RangeFilter(
        widget=RangeWidget(attrs={"type": "number", "step": "0.01", "min": "0"}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))

    class Meta:
        model = Cliente
        fields = ["detalles__sexo",
                  "estado",
                  "monto_credito",
                  "orden_cantidad",
                  "orden_monto",
                  "orden_fechas",
                  "created_at"
                  ]
        form = ClienteFilterForm

    def cantidad_ordenes(self, queryset, name, value):
        queryset = queryset.annotate(c=Count('ordenes')).order_by('-codigo')
        if value.start and value.stop:
            queryset = queryset.filter(Q(c__gte=value.start) & Q(
                c__lte=value.stop))
        else:
            if value.start:
                queryset = queryset.filter(c__gte=value.start)
            elif value.stop:
                queryset = queryset.filter(c__lte=value.stop)
        return queryset

    def ordenes_fechas(self, queryset, name, value):
        if value.start and value.stop:
            queryset = queryset.filter(
                Q(ordenes__fecha__gte=value.start) & Q(ordenes__fecha__lte=value.stop))
        else:
            if value.start:
                queryset = queryset.filter(
                    ordenes__fecha__gte=value.start)
            elif value.stop:
                queryset = queryset.filter(
                    ordenes__fecha__lte=value.stop)
        queryset = queryset.distinct()
        return queryset

    def ordenes_monto(self, queryset, name, value):
        queryset = queryset.annotate(
            monto=Sum('ordenes__valor_total')).order_by('-codigo')
        if value.start and value.stop:
            queryset = queryset.filter(
                Q(monto__gte=value.start) & Q(monto__lte=value.stop))
        else:
            if value.start:
                queryset = queryset.filter(monto__gte=value.start)
            elif value.stop:
                queryset = queryset.filter(monto__lte=value.stop)
        return queryset
