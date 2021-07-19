from urllib.parse import urlparse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import (AccessMixin, LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from neymatex.models import Empleado

from seguridad.forms import (EmpleadoEditarForm, EmpleadoForm,
                             UsuarioDetallesForm, UsuarioEditarForm,
                             UsuarioForm)

from .models import *

# Admin


def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next', None)
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect('neymatex:principal')
            else:
                messages.error(request, 'Esta cuenta ha sido desactivada.')
                return redirect('seguridad:login_admin')
        else:
            messages.error(
                request, 'Nombre de usuario o contraseña incorrecto.')
            return redirect('seguridad:login_admin')
    else:
        if request.user and request.user.is_authenticated:
            return redirect('neymatex:principal')
        else:
            return render(request, 'login.html', {"title": "Iniciar Sesión"})


def logout_user(request):
    if request.GET:
        logout(request)
        return redirect('seguridad:login_admin')


class EmpleadoPermissionRequieredMixin(PermissionRequiredMixin, AccessMixin):
    raise_exception = False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


class ListarEmpleados(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, ListView):
    paginate_by = 25
    model = Empleado
    context_object_name = 'empleados'
    template_name = "lista_empleado.html"
    permission_required = 'neymatex.view_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Empleados"
        return context


class CrearEmpleado(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    user_form_class = UsuarioForm
    user_details_form_class = UsuarioDetallesForm
    template_name = 'empleado_nuevo.html'
    title = "Crear empleado"
    success_url = reverse_lazy('seguridad:listar')
    permission_required = 'neymatex.add_empleado'

    def get_context_data(self, **kwargs):
        context = super(CrearEmpleado, self).get_context_data(**kwargs)
        if "user_form" not in context:
            context['user_form'] = self.user_form_class()
        if "user_details_form" not in context:
            context['user_details_form'] = self.user_details_form_class()
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        empleado_form = self.form_class(request.POST, request.FILES)
        usuario_form = self.user_form_class(request.POST)
        usuario_detalles_form = self.user_details_form_class(request.POST)
        if usuario_form.is_valid() and empleado_form.is_valid() and usuario_detalles_form.is_valid():
            user = usuario_form.save()
            detalles = usuario_detalles_form.save()
            empleado = empleado_form.save(commit=False)
            try:
                pre = str(int(self.model.objects.latest('pk').pk+1))
                sec = '0'*(4-len(pre))+pre
            except self.model.DoesNotExist:
                sec = '0001'
            empleado.codigo = sec
            empleado.usuario = user
            empleado.detalles = detalles
            empleado.save()
            messages.success(request, "Empleado creado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": empleado_form, "user_form": usuario_form,
                                            "user_details_form": usuario_detalles_form, "title": self.title})


class EditarEmpleado(LoginRequiredMixin, EmpleadoPermissionRequieredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoEditarForm
    user_form_class = UsuarioEditarForm
    user_details_form_class = UsuarioDetallesForm
    template_name = 'empleado_nuevo.html'
    title = "Editar empleado"
    success_url = reverse_lazy('seguridad:listar')
    permission_required = 'neymatex.change_empleado'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', None)
        print(self.object, pk)
        if "user_form" not in context:
            context['user_form'] = self.user_form_class(
                instance=self.object.usuario)
        if "user_details_form" not in context:
            context['user_details_form'] = self.user_details_form_class(
                instance=self.object.detalles)
        context['title'] = self.title
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        empleado_form = self.form_class(
            request.POST, request.FILES, instance=self.object)
        usuario_form = self.user_form_class(
            request.POST, instance=self.object.usuario)
        usuario_detalles_form = self.user_details_form_class(
            request.POST, instance=self.object.detalles)
        if usuario_form.is_valid() and empleado_form.is_valid() and usuario_detalles_form.is_valid():
            user = usuario_form.save()
            detalles = usuario_detalles_form.save()
            empleado = empleado_form.save(commit=False)
            empleado.usuario = user
            empleado.detalles = detalles
            empleado.save()
            messages.success(request, "Empleado editado con éxito.")
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response({"form": empleado_form, "user_form": usuario_form,
                                            "user_details_form": usuario_detalles_form, "title": self.title})


@login_required()
def empleado_confirmar_eliminacion(request, pk):
    empleado = Empleado.objects.get(id=pk)
    if request.POST:
        usuario = empleado.usuario
        usuario.is_active = False
        usuario.save()
        messages.success(request, "Empleado desactivado con éxito.")
        return redirect('seguridad:listar')
    return render(request, "ajax/empleado_confirmar_elminar.html", {"empleado": empleado})


@login_required()
def empleado_confirmar_activar(request, pk):
    empleado = Empleado.objects.get(id=pk)
    if request.POST:
        usuario = empleado.usuario
        usuario.is_active = True
        usuario.save()
        messages.success(request, "Empleado activado con éxito.")
        return redirect('seguridad:listar')
    return render(request, "ajax/empleado_confirmar_activar.html", {"empleado": empleado})
