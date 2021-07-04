from django import forms
from django.db.models import fields
from neymatex.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_forms.bootstrap import PrependedText


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        labels = {
            "codigo": "Código",
            "nombre": 'Nombre',
            "descripcion": 'Descripción',
            "precio": 'Precio',
            "cantidad": 'Cantidad (Stock)',
            "categoria": 'Categorías',
        }
        widgets = {
            "estado": forms.HiddenInput(),
            "is_active": forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'rows': 5}),
            "categoria": forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                'is_active',
                'estado',
                Column('categoria', css_class='col-12 d-none'),
                Column('codigo', css_class='col-12 col-lg-3'),
                Column('nombre', css_class='col-12 col-lg-5'),
                Column('descripcion', css_class='col-12 col-lg-8'),
            ),
            Row(
                Column('unidad', css_class='col-12 col-lg-2'),
                Column(PrependedText('precio', '$'),
                       css_class='col-12 col-lg-3'),
                Column('cantidad', css_class='col-12 col-lg-3'),
            ),
        )


class ProductoEditarForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        labels = {
            "nombre": 'Nombre',
            "descripcion": 'Descripción',
            "precio": 'Precio',
            "cantidad": 'Cantidad (Stock)',
            "categoria": 'Categorías',
        }
        widgets = {
            "estado": forms.Select(attrs={"disabled": True}),
            "codigo": forms.HiddenInput(),
            "is_active": forms.HiddenInput(),
            "categoria": forms.SelectMultiple(),
            'descripcion': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                'is_active',
                'codigo',
                Column('categoria', css_class='col-12 d-none'),
                Column('estado', css_class='col-12 col-lg-3'),
                Column('nombre', css_class='col-12 col-lg-5'),
                Column('descripcion', css_class='col-12 col-lg-8'),
            ),
            Row(
                Column('unidad', css_class='col-12 col-lg-2'),
                Column(PrependedText('precio', '$'),
                       css_class='col-12 col-lg-3'),
                Column('cantidad', css_class='col-12 col-lg-3'),
            ),
        )
