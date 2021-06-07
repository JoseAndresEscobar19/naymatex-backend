from neymatex.models import Empleado
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView

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
                    return redirect('principal')
            else:
                messages.error(request, 'Esta cuenta ha sido desactivada.')
                return redirect('login_admin')
        else:
            messages.error(
                request, 'Nombre de usuario o contraseña incorrecto.')
            return redirect('login_admin')
    return render(request, 'login.html', {"title": "Iniciar Sesión"})


def logout_user(request):
    if request.GET:
        logout(request)
        return redirect('login_admin')


class ListarEmpleados(LoginRequiredMixin, ListView):
    # required_permission = 'seguridad'
    model = Empleado
    context_object_name = 'empleados'
    template_name = "lista_empleado.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Empleados"
        return context


def empleado_confirmar_eliminacion(request, pk):
    # empleado=Empleado.objects.get(id=pk)
    # form=OrdenFacturacionForm(instance=orden)
    return render(request, "ajax/empleado_confirmar_elminar.html")
