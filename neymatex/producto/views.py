import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from neymatex.models import *
from neymatex.serializers import TipoCategoriaSerializer
from seguridad.views import EmpleadoPermissionRequieredMixin

from .forms import ProductoEditarForm, ProductoForm


# Create your views here.
# PRODUCTO
class ListarProductos(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, ListView):
    # required_permission = 'seguridad'
    paginate_by = 25
    model = Producto
    context_object_name = 'productos'
    template_name = "lista_producto.html"
    permission_required = 'neymatex.view_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Producto"
        return context


class CrearProducto(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_nuevo.html'
    title = "Crear producto"
    success_url = reverse_lazy('neymatex:producto:listar')
    permission_required = 'neymatex.view_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        tipo_categoria = []
        for tipo in TipoCategoria.objects.all():
            tipo_categoria.append(json.loads(
                json.dumps(TipoCategoriaSerializer(tipo).data)))
        context['tipos_categoria'] = tipo_categoria
        return context


class EditarProducto(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, UpdateView):
    model = Producto
    form_class = ProductoEditarForm
    template_name = 'producto_nuevo.html'
    title = "Editar producto"
    success_url = reverse_lazy('neymatex:producto:listar')
    permission_required = 'neymatex.view_producto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        tipo_categoria = []
        for tipo in TipoCategoria.objects.all():
            tipo_categoria.append(json.loads(
                json.dumps(TipoCategoriaSerializer(tipo).data)))
        context['tipos_categoria'] = tipo_categoria
        return context


@login_required()
def producto_confirmar_eliminacion(request, pk):
    producto = Producto.objects.get(id=pk)
    if request.POST:
        producto.is_active = False
        producto.estado = Producto.Status.DISABLED
        producto.save()
        messages.success(request, "Producto deshabilitado con éxito.")
        return redirect('neymatex:producto:listar')
    return render(request, "ajax/producto_confirmar_elminar.html", {"producto": producto})


@login_required()
def producto_confirmar_activar(request, pk):
    producto = Producto.objects.get(id=pk)
    if request.POST:
        producto.is_active = True
        if producto.cantidad > 0:
            producto.estado = Producto.Status.INSTOCK
        else:
            producto.estado = Producto.Status.OUTSTOCK
        producto.save()
        messages.success(request, "Producto habilitado con éxito.")
        return redirect('neymatex:producto:listar')
    return render(request, "ajax/producto_confirmar_activar.html", {"producto": producto})
