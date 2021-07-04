from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from seguridad.forms import UsuarioDetallesForm

from .forms import ClienteEditarForm, ClienteForm

from neymatex.models import *


# Create your views here.
class ListarClientes(LoginRequiredMixin, ListView):
    # required_permission = 'seguridad'
    model = Cliente
    context_object_name = 'clientes'
    template_name = "lista_cliente.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Clientes"
        return context


class CrearCliente(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    user_details_form_class = UsuarioDetallesForm
    template_name = 'cliente_nuevo.html'
    title = "Crear cliente"
    success_url = reverse_lazy('neymatex:cliente:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "user_details_form" not in context:
            context['user_details_form'] = self.user_details_form_class()
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        cliente_form = self.form_class(request.POST)
        usuario_detalles_form = self.user_details_form_class(request.POST)
        if cliente_form.is_valid() and usuario_detalles_form.is_valid():
            detalles = usuario_detalles_form.save()
            cliente = cliente_form.save(commit=False)
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            cliente.codigo = sec
            cliente.detalles = detalles
            cliente.save()
            messages.success(request, "Cliente creado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": cliente_form, "user_details_form": usuario_detalles_form, "title": self.title})

    def form_valid(self, form):
        try:
            pre = str(int(self.model.objects.latest('pk').pk+1))
            sec = '0'*(4-len(pre))+pre
        except self.model.DoesNotExist:
            sec = '0001'
        form.instance.codigo = sec
        return super().form_valid(form)


class EditarCliente(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteEditarForm
    user_details_form_class = UsuarioDetallesForm
    template_name = 'cliente_nuevo.html'
    title = "Editar Cliente"
    success_url = reverse_lazy('neymatex:cliente:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "user_details_form" not in context:
            context['user_details_form'] = self.user_details_form_class(
                instance=self.object.detalles)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        cliente_form = self.form_class(request.POST, instance=self.object)
        detalles_form = self.user_details_form_class(
            request.POST, instance=self.object.detalles)
        if cliente_form.is_valid() and detalles_form.is_valid():
            detalles = detalles_form.save()
            cliente = cliente_form.save(commit=False)
            cliente.detalles = detalles
            cliente.save()
            messages.success(request, "Cliente editado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": cliente_form, "user_details_form": detalles_form, "title": self.title})


def cliente_confirmar_eliminacion(request, pk):
    cliente = Cliente.objects.get(id=pk)
    if request.POST:
        cliente.is_active = False
        cliente.save()
        messages.success(request, "Cliente desactivado con éxito.")
        return redirect('neymatex:cliente:listar')
    return render(request, "ajax/cliente_confirmar_elminar.html", {"cliente": cliente})


def cliente_confirmar_activar(request, pk):
    cliente = Cliente.objects.get(id=pk)
    if request.POST:
        cliente.is_active = True
        cliente.save()
        messages.success(request, "Cliente activado con éxito.")
        return redirect('neymatex:cliente:listar')
    return render(request, "ajax/cliente_confirmar_activar.html", {"cliente": cliente})
