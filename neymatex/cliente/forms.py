from crispy_forms.bootstrap import PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Reset, Row
from django import forms
from neymatex.models import *


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ('detalles',)
        labels = {
            "monto_credito": "Monto Crédito"
        }
        widgets = {
            "codigo": forms.HiddenInput(),
            "estado": forms.HiddenInput(),
            "is_active": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Div(
                    'codigo',
                    'estado',
                    'is_active',
                ),
                Column(
                    PrependedText('monto_credito', '$',
                                  placeholder=""),
                    css_class='col-lg-4 col-6'
                ),
            ),
        )


class ClienteEditarForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ('detalles',)
        labels = {
            "monto_credito": "Monto Crédito",
            "codigo": ''
        }
        widgets = {
            "codigo": forms.HiddenInput(),
            "is_active": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                'codigo',
                'is_active',
                Column(
                    PrependedText('monto_credito', '$',
                                  placeholder=""),
                    css_class='col-xl-4 col-6'
                ),
                Column('estado', css_class='col-6 col-xl-4')
            ),
        )


class ClienteFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.fields['orden_cantidad'].label = "Cantidad de órdenes"
        self.fields['orden_fechas'].label = "Fechas de compra"
        self.fields['orden_monto'].label = "Monto de compra"
        self.fields['detalles__sexo'].label = "Sexo del cliente"
        self.fields['monto_credito'].label = "Monto aprobado de crédito"
        self.fields['created_at'].label = "Fecha de creación"

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-lg-6'
                ),
                Column('detalles__sexo', css_class='col-6 col-lg-3'),
                Column('estado', css_class='col-6 col-lg-3'),
                Column(
                    Field('orden_fechas',
                          template="forms/fields/range-filter.html", css_class="form-control"),
                    css_class='col-12 col-lg-6'
                ),
                Column(
                    Field('orden_monto',
                          template="forms/fields/range-filter.html", css_class="form-control", placeholder="$"),
                    css_class='col-12 col-lg-6'
                ),
                Column(
                    Field('orden_cantidad',
                          template="forms/fields/range-filter.html", css_class="form-control"),
                    css_class='col-12 col-lg-3'
                ),
                Column(
                    Field('monto_credito', template="forms/fields/range-filter.html",
                          css_class="form-control", placeholder="$"),
                    css_class='col-lg-3 col-6'
                ),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )
