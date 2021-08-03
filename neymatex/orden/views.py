import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.detail import DetailView
from neymatex.models import *
from neymatex.serializers import TipoCategoriaSerializer
from neymatex.viewsets import TipoCategoriaView
from rest_framework.response import Response
from seguridad.views import EmpleadoPermissionRequieredMixin

from .forms import DetallesOrdenFormset, OrdenEditarForm, OrdenObservacionForm


# Create your views here.
# PEDIDOS
class ListarOrdenes(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, ListView):
    paginate_by = 25
    model = Orden
    context_object_name = 'ordenes'
    template_name = "lista_orden.html"
    permission_required = 'neymatex.view_orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Orden"
        return context


class VerOrden(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, DetailView):
    model = Orden
    context_object_name = 'orden'
    template_name = 'orden_ver.html'
    title = "Detalles Pedido"
    success_url = reverse_lazy('neymatex:producto:listar')
    permission_required = 'neymatex.view_orden'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['productos'] = self.get_object().detalles.all()
        return context


class EditarOrden(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, UpdateView):
    model = Orden
    form_class = OrdenEditarForm
    formset_class = DetallesOrdenFormset
    context_object_name = 'orden'
    template_name = 'orden_editar.html'
    title = "Editar Pedido"
    permission_required = 'neymatex.change_orden'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['orden'] = self.object
        context['productos'] = self.object.detalles.all()
        context['formset'] = self.formset_class(
            queryset=self.object.detalles.all())
        context['detalles'] = zip(context['productos'], context['formset'])
        return context

    def get_success_url(self):
        return reverse('neymatex:orden:ver', args=[self.get_object().pk])

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        orden_form = self.form_class(request.POST, instance=self.object)
        detalles_form = self.formset_class(
            request.POST, queryset=self.object.detalles.all())
        if orden_form.is_valid() and detalles_form.is_valid():
            orden_form.save()
            detalles_form.save()
            # @TODO Calcular totales usando valores especiales o normales
            # @TODO Crear/enviar notificacion al vendedor de la orden que se esta modificando
            messages.success(
                request, "Se ha editado el pedido con éxito. Notificación enviada al vendedor")
            return HttpResponseRedirect(self.get_success_url())
        else:
            context = self.get_context_data()
            context['formset'] = detalles_form
            context['detalles'] = zip(context['productos'], context['formset'])
            return self.render_to_response(context)


@login_required()
def orden_confirmar_eliminacion(request, pk):
    orden = Orden.objects.get(id=pk)
    if request.POST:
        orden.estado = Orden.Status.CANCEL
        orden.save()
        messages.success(request, "¡¡Pedido cancelado!!")
        return redirect('neymatex:orden:listar')
    return render(request, "ajax/orden_confirmar_elminar.html", {"orden": orden})


@login_required()
def orden_confirmar_pagar(request, pk):
    orden = Orden.objects.get(id=pk)
    if request.POST:
        orden.estado = Orden.Status.PAID
        orden.save()
        messages.success(request, "¡¡Pedido Pagado!!")
        return redirect('neymatex:orden:listar')
    return render(request, "ajax/orden_confirmar_pagar.html", {"orden": orden})


@login_required()
def orden_observacion(request, pk):
    orden = Orden.objects.get(id=pk)
    context = {"orden": orden}
    if request.POST:
        form = OrdenObservacionForm(request.POST, instance=orden)
        if form.is_valid():
            form.save()
            messages.success(request, "Se agregó la observación al pedido")
            return redirect('neymatex:orden:ver', pk)
        else:
            context['form'] = form
            return render(request, "ajax/orden_observaciones.html", context, status=400)
    else:
        context['form'] = OrdenObservacionForm(instance=orden)
    return render(request, "ajax/orden_observaciones.html", context)
