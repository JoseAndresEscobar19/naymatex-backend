import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from neymatex.models import *
from neymatex.serializers import TipoCategoriaSerializer
from neymatex.viewsets import TipoCategoriaView
from rest_framework.response import Response
from seguridad.views import EmpleadoPermissionRequieredMixin

from .forms import OrdenForm


# Create your views here.
# PEDIDOS
class ListarOrdenes(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, ListView):
    model = Orden
    context_object_name = 'ordenes'
    template_name = "lista_orden.html"
    permission_required = 'neymatex.view_orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Orden"
        return context


# class CrearProducto(LoginRequiredMixin, CreateView):
#     model = Producto
#     form_class = ProductoForm
#     template_name = 'producto_nuevo.html'
#     title = "Crear producto"
#     success_url = reverse_lazy('neymatex:producto:listar')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = self.title
#         tipo_categoria = []
#         for tipo in TipoCategoria.objects.all():
#             tipo_categoria.append(json.loads(
#                 json.dumps(TipoCategoriaSerializer(tipo).data)))
#         context['tipos_categoria'] = tipo_categoria
#         return context


class VerOrden(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, DetailView):
    model = Orden
    context_object_name = 'orden'
    template_name = 'orden_ver.html'
    title = "Pedido"
    success_url = reverse_lazy('neymatex:producto:listar')
    permission_required = 'neymatex.view_orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['productos'] = self.get_object().detalles.all()
        return context

    # def post(self, request, *args, **kwargs):
        # print(request.POST)
        # return super().post(request, *args, **kwargs)

        # self.object = self.get_object()
        # cliente_form = self.form_class(request.POST, instance=self.object)
        # detalles_form = self.user_details_form_class(
        #     request.POST, instance=self.object.detalles)
        # if cliente_form.is_valid() and detalles_form.is_valid():
        #     detalles = detalles_form.save()
        #     cliente = cliente_form.save(commit=False)
        #     cliente.detalles = detalles
        #     cliente.save()
        #     messages.success(request, "Cliente editado con éxito.")
        #     return HttpResponseRedirect(self.success_url)
        # else:
        #     return self.render_to_response({"form": cliente_form, "user_details_form": detalles_form, "title": self.title})


@login_required()
def orden_confirmar_eliminacion(request, pk):
    orden = Orden.objects.get(id=pk)
    if request.POST:
        orden.estado = Orden.Status.CANCEL
        orden.save()
        messages.success(request, "¡¡Pedido cancelado!!")
        return redirect('neymatex:orden:listar')
    return render(request, "ajax/orden_confirmar_elminar.html", {"orden": orden})


# def producto_confirmar_activar(request, pk):
#     producto = Producto.objects.get(id=pk)
#     if request.POST:
#         producto.is_active = True
#         if producto.cantidad > 0:
#             producto.estado = Producto.Status.INSTOCK
#         else:
#             producto.estado = Producto.Status.OUTSTOCK
#         producto.save()
#         messages.success(request, "Producto habilitado con éxito.")
#         return redirect('neymatex:producto:listar')
#     return render(request, "ajax/producto_confirmar_activar.html", {"producto": producto})
