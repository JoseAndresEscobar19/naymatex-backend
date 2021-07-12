from django import forms
from django.db.models import fields
from neymatex.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_forms.bootstrap import AppendedText, PrependedText


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
            "imagen": 'Imagen',
            "composicion": 'Composición',
            "precioMetro": 'Precio por metro',
            "precioMetroEspecial": 'Precio por metro Especial',
            "precioRollo": 'Precio por rollo',
            "precioRolloEspecial": 'Precio por rollo Especial',
        }
        widgets = {
            "estado": forms.HiddenInput(),
            "is_active": forms.HiddenInput(),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'uso': forms.Textarea(attrs={'rows': 2}),
            "categoria": forms.SelectMultiple(),
            "imagen": forms.FileInput()
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
                Column('codigo', css_class='col-12 col-lg-4'),
                Column('nombre', css_class='col-12 col-lg-8'),
                Column('descripcion', css_class='col-12 col-lg-12'),
                Column('uso', css_class='col-12 col-lg-12'),
                Column('composicion', css_class='col-12 col-lg-12'),
            ),
            Row(
                Column('unidad', css_class='col-12 col-lg-4'),
                Column('cantidad', css_class='col-12 col-lg-4'),
                Column(AppendedText('ancho', 'm'),
                       css_class='col-12 col-lg-4'),
                Column(PrependedText('precioMetro', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioMetroEspecial', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioRollo', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioRolloEspecial', '$'),
                       css_class='col-12 col-lg-6'),
                Column('imagen', css_class='col-12 col-lg-6'),
            ),
        )


class ProductoEditarForm(forms.ModelForm):
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
            "composicion": 'Composición',
            "precioMetro": 'Precio por metro',
            "precioMetroEspecial": 'Precio por metro Especial',
            "precioRollo": 'Precio por rollo',
            "precioRolloEspecial": 'Precio por rollo Especial',
        }
        widgets = {
            "estado": forms.Select(attrs={"disabled": True}),
            "is_active": forms.HiddenInput(),
            "categoria": forms.SelectMultiple(),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'uso': forms.Textarea(attrs={'rows': 2}),
            "imagen": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                'is_active',
                Column('categoria', css_class='col-12 d-none'),
                Column('estado', css_class='col-12 col-lg-3'),
                Column('codigo', css_class='col-12 col-lg-3'),
                Column('nombre', css_class='col-12 col-lg-6'),
                Column('descripcion', css_class='col-12 col-lg-12'),
                Column('uso', css_class='col-12 col-lg-12'),
                Column('composicion', css_class='col-12 col-lg-12'),
            ),
            Row(
                Column('unidad', css_class='col-12 col-lg-4'),
                Column('cantidad', css_class='col-12 col-lg-4'),
                Column(AppendedText('ancho', 'm'),
                       css_class='col-12 col-lg-4'),
                Column(PrependedText('precioMetro', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioMetroEspecial', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioRollo', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioRolloEspecial', '$'),
                       css_class='col-12 col-lg-6'),
                Column('imagen', css_class='col-12'),
            ),
        )
