from neymatex.utils import export_excel, export_pdf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django_filters.views import FilterView
from neymatex.models import *
from seguridad.forms import UsuarioDetallesForm
from seguridad.views import EmpleadoPermissionRequieredMixin

from .filters import ClienteFilter
from .forms import ClienteEditarForm, ClienteForm

# Create your views here.


class ListarClientes(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, FilterView):
    paginate_by = 20
    model = Cliente
    context_object_name = 'clientes'
    template_name = "lista_cliente.html"
    permission_required = 'neymatex.view_cliente'
    filterset_class = ClienteFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Clientes"
        return context

    def get(self, request, *args, **kwargs):
        if request.GET.get("export"):
            queryset = self.filterset_class(request.GET,
                                            queryset=self.model.objects.all()).qs
            tipo = request.GET.get("export")
            columns = {
                'Código': '5%',
                'Cédula': '7%',
                'Nombres': 'auto',
                'Apellidos': 'auto',
                'Teléfono': '7%',
                'Teléfono 2': '7%',
                'Direccion': 'auto',
                'Sexo': '3%',
                'Estado': '4%',
                'Monto crédito': '7%',
                'Fecha de registro': '10%',
            }
            fields = [
                'codigo',
                'detalles__cedula',
                'detalles__nombres',
                'detalles__apellidos',
                'detalles__telefono',
                'detalles__telefono2',
                'detalles__direccion',
                'detalles__sexo',
                'estado',
                'monto_credito',
                'created_at',
            ]
            if tipo == "pdf":
                return export_pdf(columns, queryset.values_list(*fields), 'clientes')
            elif tipo == "xlsx":
                return export_excel(columns, queryset.values_list(*fields), 'clientes')
        return super().get(request, *args, **kwargs)


class CrearCliente(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    user_details_form_class = UsuarioDetallesForm
    template_name = 'cliente_nuevo.html'
    title = "Crear cliente"
    success_url = reverse_lazy('neymatex:cliente:listar')
    permission_required = 'neymatex.add_cliente'

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


class EditarCliente(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, UpdateView):
    model = Cliente
    form_class = ClienteEditarForm
    user_details_form_class = UsuarioDetallesForm
    template_name = 'cliente_nuevo.html'
    title = "Editar Cliente"
    success_url = reverse_lazy('neymatex:cliente:listar')
    permission_required = 'neymatex.change_cliente'

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


@login_required()
def cliente_confirmar_eliminacion(request, pk):
    cliente = Cliente.objects.get(id=pk)
    if request.POST:
        cliente.is_active = False
        cliente.save()
        messages.success(request, "Cliente desactivado con éxito.")
        return redirect('neymatex:cliente:listar')
    return render(request, "ajax/cliente_confirmar_elminar.html", {"cliente": cliente})


@login_required()
def cliente_confirmar_activar(request, pk):
    cliente = Cliente.objects.get(id=pk)
    if request.POST:
        cliente.is_active = True
        cliente.save()
        messages.success(request, "Cliente activado con éxito.")
        return redirect('neymatex:cliente:listar')
    return render(request, "ajax/cliente_confirmar_activar.html", {"cliente": cliente})
