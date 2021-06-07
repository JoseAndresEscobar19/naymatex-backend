from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required

# Admin.


@login_required
def home(request):
    return render(request, 'principal.html', {'title': 'Principal'})
