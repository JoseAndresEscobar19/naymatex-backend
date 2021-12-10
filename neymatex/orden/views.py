import io

import xlsxwriter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.utils import timezone
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView
from django_filters.views import FilterView
from neymatex.models import *
from neymatex.orden.filters import OrdenFilter
from neymatex.utils import calculate_pages_to_render, pdf_orden, print_file
from seguridad.views import EmpleadoPermissionRequieredMixin

from .forms import DetallesOrdenFormset, OrdenEditarForm, OrdenObservacionForm


# Create your views here.
# PEDIDOS
class ListarOrdenes(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, FilterView):
    paginate_by = 20
    max_pages_render = 10
    model = Orden
    context_object_name = 'ordenes'
    template_name = "lista_orden.html"
    permission_required = 'neymatex.view_orden'
    filterset_class = OrdenFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Orden"
        page_obj = context["page_obj"]
        context['num_pages'] = calculate_pages_to_render(self, page_obj)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        # groups = self.request.user.groups.all().values_list('name', flat=True)
        # if "Gerente" in groups or self.request.user.is_superuser:
        #     return queryset

        # if "Caja" in groups:
        #     estado = Orden.Status.NOPAG
        # elif "Despacho" in groups:
        #     estado = Orden.Status.PAID
        # return queryset.filter(estado=estado)


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
            for d_form in detalles_form:
                detalle = d_form.save(commit=False)
                detalle.calcular_valor_total_detalle()
                detalle.save()
            orden = orden_form.save(commit=False)
            orden.calcular_todo()
            orden.save()
            notificacion = Notificacion(title="Se ha actualizado uno de tus pedidos",
                                        body="El pedido {} fue actualizado por {}. Motivo: {}".format(orden.codigo, self.request.user, orden.observaciones))
            notificacion.save()
            orden.empleado.usuario.notificaciones.add(notificacion)
            messages.success(
                request, "Se ha editado el pedido con éxito. Notificación enviada al vendedor")
            rutas = pdf_orden(orden)
            print_file(rutas[0])
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
        if orden.validar_stock_orden() and request.user.empleado.all().count() and request.user.groups.filter(name="Caja").exists():
            orden.estado = Orden.Status.PAID
            orden.cajero = request.user.empleado.all()[0]
            orden.fecha_pagado = timezone.now().astimezone()
            orden.reducir_stock_orden()
            orden.save()
            messages.success(request, "¡¡Pedido Pagado!!")
            return redirect('neymatex:orden:listar')
        else:
            messages.error(
                request, "Ha ocurrido un error en la transacción. Verifique su usuario")
            for detalle in orden.detalles.all():
                if not detalle.validar_stock_items():
                    messages.error(request, "No existe stock para {}. Verifique el pedido e intente nuevamente.".format(
                        detalle.producto.nombre))
            return redirect('neymatex:orden:ver', pk)
    return render(request, "ajax/orden_confirmar_pagar.html", {"orden": orden})


@login_required()
def orden_confirmar_despachar(request, pk):
    orden = Orden.objects.get(id=pk)
    if request.POST:
        if request.user.empleado.all().count() and request.user.groups.filter(name="Despacho").exists():
            orden.estado = Orden.Status.DES
            orden.despachador = request.user.empleado.all()[0]
            orden.fecha_despachado = timezone.now().astimezone()
            orden.save()
            messages.success(request, "¡¡Pedido Despachado!!")
            return redirect('neymatex:orden:listar')
        else:
            messages.error(
                request, "Ha ocurrido un error en la transacción. Verifique su usuario")
            return redirect('neymatex:orden:ver', pk)
    return render(request, "ajax/orden_confirmar_despachar.html", {"orden": orden})


@ login_required()
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
