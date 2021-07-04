import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from neymatex.models import *
from neymatex.viewsets import TipoCategoriaView
from rest_framework.response import Response

from .forms import ProductoEditarForm, ProductoForm


# Create your views here.
# PRODUCTO
class ListarProductos(LoginRequiredMixin, ListView):
    # required_permission = 'seguridad'
    model = Producto
    context_object_name = 'productos'
    template_name = "lista_producto.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Producto"
        return context


class CrearProducto(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto_nuevo.html'
    title = "Crear producto"
    success_url = reverse_lazy('neymatex:producto:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['tipos_categoria'] = json.loads(json.dumps(TipoCategoriaView.as_view(
            {'get': 'list', 'post': 'list'})(self.request).data))
        return context


class EditarProducto(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoEditarForm
    template_name = 'producto_nuevo.html'
    title = "Editar producto"
    success_url = reverse_lazy('neymatex:producto:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['tipos_categoria'] = json.loads(json.dumps(TipoCategoriaView.as_view(
            {'get': 'list', 'post': 'list'})(self.request).data))
        return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         cliente_form = self.form_class(request.POST, instance=self.object)
#         detalles_form = self.user_details_form_class(
#             request.POST, instance=self.object.detalles)
#         if cliente_form.is_valid() and detalles_form.is_valid():
#             detalles = detalles_form.save()
#             cliente = cliente_form.save(commit=False)
#             cliente.detalles = detalles
#             cliente.save()
#             messages.success(request, "Cliente editado con éxito.")
#             return HttpResponseRedirect(self.success_url)
#         else:
#             return self.render_to_response({"form": cliente_form, "user_details_form": detalles_form, "title": self.title})


def producto_confirmar_eliminacion(request, pk):
    producto = Producto.objects.get(id=pk)
    if request.POST:
        producto.is_active = False
        producto.estado = Producto.Status.DISABLED
        producto.save()
        messages.success(request, "Producto deshabilitado con éxito.")
        return redirect('neymatex:producto:listar')
    return render(request, "ajax/producto_confirmar_elminar.html", {"producto": producto})


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
