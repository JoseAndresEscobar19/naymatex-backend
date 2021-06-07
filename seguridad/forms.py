from django import forms
from neymatex.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm


class EmpleadoForm(UserCreationForm):
    class Meta:
        model = Empleado
        fields = [
            'cedula',
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
            'email',
            'telefono',
            'estado',
            'sexo',
            'area',
            'cargo',
            'imagen',
            'observaciones'

        ]

    def add_prefix(self, field_name):
        field_name_mapping = {
            'first_name': 'nombre',
            'last_name': 'apellido',
        }
        field_name = field_name_mapping.get(field_name, field_name)
        return super(EmpleadoForm, self).add_prefix(field_name)
