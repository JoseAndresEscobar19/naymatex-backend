from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import *

# Admin.


@login_required
def home(request):
    return render(request, 'principal.html', {'title': 'Principal'})
