import django_filters
from django.db.models import Q
from django.db.models.aggregates import Count, Sum
from django_filters.widgets import RangeWidget
from neymatex.models import *
from neymatex.orden.forms import OrdenFilterForm


class OrdenFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}))

    class Meta:
        model = Orden
        fields = ["created_at",
                  "estado",
                  # "monto_credito",
                  # "orden_cantidad",
                  # "orden_monto",
                  # "orden_fechas",
                  ]
        form = OrdenFilterForm
