from django.shortcuts import render
from .models import *

# Admin.


def home(request):
    return render(request, 'principal.html')
