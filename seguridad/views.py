from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
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
                messages.error(request, 'Esta cuenta ha sido desactivada')
                return redirect('login')
        else:
            messages.error(
                request, 'Nombre de usuario o contraseña incorrecto')
            return redirect('login')
    return render(request, 'login.html')
