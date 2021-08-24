import django_filters
from neymatex.models import *
from neymatex.producto.forms import ProductoFilterForm


class ProductoFilter(django_filters.FilterSet):
    class Meta:
        model = Producto
        fields = {"nombre": ["icontains"],
                  "alias": ["icontains"],
                  }
        form = ProductoFilterForm
