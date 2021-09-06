from crispy_forms.bootstrap import AppendedText, PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row
from django import forms
from django.db.models import fields
from neymatex.models import *


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        labels = {
            "codigo": "Código",
            "nombre": 'Nombre',
            "alias": 'Alias',
            "uso": 'Uso del Producto',
            "precio": 'Precio',
            "cantidad_metro": 'Cantidad metros por rollo',
            "cantidad_rollo": 'Cantidad de rollos',
            "categoria": 'Estilos',
            "imagen": 'Imagen',
            "composicion": 'Composición',
            "precioMetro": 'Precio por metro Máx',
            "precioMetroEspecial": 'Precio por metro Min',
        }
        widgets = {
            "estado": forms.HiddenInput(),
            "is_active": forms.HiddenInput(),
            "total_metros": forms.HiddenInput(),
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
                'total_metros',
                Column('codigo', css_class='col-12 col-lg-4'),
                Column('nombre', css_class='col-12 col-lg-8'),
                Column('alias', css_class='col-12'),
                Column(Field('categoria', multiple="true",
                             css_class="select2"), css_class='col-12'),
                Column('uso', css_class='col-12 col-lg-12'),
                Column('composicion', css_class='col-12 col-lg-12'),
            ),
            Row(
                Column('unidad', css_class='col-12 col-lg-6'),
                Column(AppendedText('ancho', 'm'),
                       css_class='col-12 col-lg-6'),
                Column(AppendedText('cantidad_metro', 'm'),
                       css_class='col-12 col-lg-6'),
                Column(Field('cantidad_rollo', readonly=True),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioMetroEspecial', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioMetro', '$'),
                       css_class='col-12 col-lg-6'),

                Column('imagen', css_class='col-12'),
            ),
        )


class ProductoEditarForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        labels = {
            "codigo": "Código",
            "nombre": 'Nombre',
            "alias": 'Alias',
            "uso": 'Uso del Producto',
            "precio": 'Precio',
            "cantidad_metro": 'Cantidad metros por rollo',
            "cantidad_rollo": 'Cantidad de rollos',
            "categoria": 'Estilos',
            "composicion": 'Composición',
            "precioMetro": 'Precio por metro Máx',
            "precioMetroEspecial": 'Precio por metro Min',
            "total_metros": "Metros restantes",
        }
        widgets = {
            "estado": forms.Select(attrs={"disabled": True}),
            "is_active": forms.HiddenInput(),
            "categoria": forms.SelectMultiple(),
            'uso': forms.Textarea(attrs={'rows': 2}),
            "imagen": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["total_metros"].help_text = "Se actualiza automáticamente"
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                'is_active',
                Column('estado', css_class='col-12 col-lg-3'),
                Column('codigo', css_class='col-12 col-lg-3'),
                Column('nombre', css_class='col-12 col-lg-6'),
                Column('alias', css_class='col-12'),
                Column(Field('categoria', multiple="true",
                             css_class="select2"), css_class='col-12'),
                Column('uso', css_class='col-12 col-lg-12'),
                Column('composicion', css_class='col-12 col-lg-12'),
            ),
            Row(
                Column('unidad', css_class='col-12 col-lg-6'),
                Column(AppendedText('ancho', 'm'),
                       css_class='col-12 col-lg-6'),
                Column(AppendedText('cantidad_metro', 'm'),
                       css_class='col-12 col-lg-6'),
                Column(Field('cantidad_rollo', readonly=True),
                       css_class='col-12 col-lg-6'),
                Column(Field('total_metros', readonly=True), css_class='col-6'),
            ),
            Row(
                Column(PrependedText('precioMetroEspecial', '$'),
                       css_class='col-12 col-lg-6'),
                Column(PrependedText('precioMetro', '$'),
                       css_class='col-12 col-lg-6'),
                Column('imagen', css_class='col-12'),
            ),
        )


class ProductoFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.fields['nombre__icontains'].label = "Nombre Producto"
        self.fields['alias__icontains'].label = "Alias del producto"
        self.helper.layout = Layout(
            Row(
                Column('nombre__icontains', css_class='col-6 col-lg-3'),
                Column('alias__icontains', css_class='col-6 col-lg-3'),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )
