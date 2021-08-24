import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django_filters.views import FilterView
from neymatex.models import *
from neymatex.producto.filter import ProductoFilter
from neymatex.serializers import TipoCategoriaSerializer
from seguridad.views import EmpleadoPermissionRequieredMixin

from .forms import ProductoEditarForm, ProductoForm


# Create your views here.
# PRODUCTO
class ListarProductos(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, FilterView):
    paginate_by = 20
    model = Producto
    context_object_name = 'productos'
    template_name = "lista_producto.html"
    permission_required = 'neymatex.view_producto'
    filterset_class = ProductoFilter

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

    def post(self, request, *args, **kwargs):
        self.object = None
        producto_form = self.form_class(request.POST)
        if producto_form.is_valid():
            producto = producto_form.save(commit=False)
            producto.total_metros = producto.cantidad_metro*producto.cantidad_rollo
            producto.save()
            messages.success(request, "Producto creado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            context = self.get_context_data()
            context["form"] = producto_form
            return self.render_to_response(context)


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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        actualizar_stock = not(int(request.POST.get('cantidad_metro')) == self.object.cantidad_metro
                               and int(request.POST.get('cantidad_rollo')) == self.object.cantidad_rollo)
        producto_form = self.form_class(request.POST, instance=self.object)
        if producto_form.is_valid():
            producto = producto_form.save(commit=False)
            if actualizar_stock:
                producto.total_metros = producto.cantidad_metro * \
                    (producto.cantidad_rollo or 1)
            producto.save()
            messages.success(request, "Producto editado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            context = self.get_context_data()
            context["form"] = producto_form
            return self.render_to_response(context)


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
