from django.contrib.auth.models import Group
import django_filters
from django.db.models import Q
from django.db.models.aggregates import Sum
from django_filters.widgets import RangeWidget
from neymatex.models import Empleado

from seguridad.forms import EmpleadoFilterForm


class EmpleadoFilter(django_filters.FilterSet):
    orden_monto = django_filters.RangeFilter(method="ordenes_monto", widget=RangeWidget(
        attrs={"type": "number", "step": "0.01", "min": "0"}))
    orden_fechas = django_filters.DateFromToRangeFilter(
        method="ordenes_fechas", widget=RangeWidget(attrs={"type": "date"}))
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))
    rol = django_filters.ModelChoiceFilter(
        queryset=Group.objects.all(), field_name='usuario__groups')

    class Meta:
        model = Empleado
        fields = ["detalles__sexo",
                  "estado",
                  "orden_monto",
                  "rol",
                  "orden_fechas",
                  "created_at",
                  ]
        form = EmpleadoFilterForm

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
