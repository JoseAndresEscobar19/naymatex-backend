from crispy_forms.bootstrap import AppendedText, PrependedText, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Field, Layout, Row
from django import forms
from django.forms.models import modelformset_factory
from neymatex.models import *


class OrdenEditarForm(forms.ModelForm):
    class Meta:
        model = Orden
        exclude = ('subtotal', 'iva', 'descuento', 'valor_total')
        labels = {
            "codigo": "Código",
            "estado": 'Estado del Pedido',
            "cliente_referencial": "Nombre referencial de la orden",
            "empleado": "Vendedor"
        }
        widgets = {
            "codigo": forms.HiddenInput(),
            "estado": forms.HiddenInput(),
            "observaciones": forms.widgets.Textarea(attrs={"rows": "3"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.fields['observaciones'].label = "Motivos de cambio"
        self.fields['observaciones'].required = True
        self.fields['observaciones'].help_text = "Especifique las razones de la modificación."
        self.helper.layout = Layout(
            'codigo',
            'estado',
            Column('cliente_referencial', css_class='col-12 col-lg-6'),
            Column(Field('cliente', css_class="select2"),
                   css_class='col-12 col-lg-6'),
            Column(Field('empleado', css_class="select2"),
                   css_class='col-12 col-lg-6'),
            Column('observaciones'),
        )


class OrdenObservacionForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = {'observaciones'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.fields['observaciones'].label = ''
        self.fields['observaciones'].required = True
        self.helper.layout = Layout(
            Row(
                Column(Field('observaciones', css_class=""),
                       css_class='col-12'),
            )
        )


class DetalleOrdenForm(forms.ModelForm):
    class Meta:
        model = DetalleOrden
        fields = '__all__'
        labels = {
            'valor_metro': 'Precio del metro',
            'valor_rollo': 'Precio del rollo',
        }
        widgets = {
            'orden': forms.HiddenInput(),
            'valor_total': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'id',
            'orden',
            'valor_total',
            Column(Field('producto', css_class="select2 update-image"),
                   css_class="col-12 col-md-6"),
            Column(AppendedText('cantidad_metro', 'm'),
                   css_class="col-xl-3 col-md-3 col-6"),
            Column('cantidad_rollo', css_class="col-xl-3 col-md-3 col-6"),
            Column(PrependedText('valor_metro', '$'),
                   css_class="col-xl-3 col-md-3 col-6"),
            Column(PrependedText('valor_rollo', '$'),
                   css_class="col-xl-3 col-md-3 col-6"),
            Column('precioMetroEspecial', css_class="col-auto"),
            Column('precioRolloEspecial', css_class="col-auto"),
        )


DetallesOrdenFormset = modelformset_factory(
    model=DetalleOrden, extra=0, form=DetalleOrdenForm,)


class OrdenFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.fields['created_at'].label = "Fecha de creación"
        self.fields['empleado'].label = "Vendedor"

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('created_at', template="forms/fields/range-filter.html",
                          css_class="form-control"), css_class='col-12 col-lg-6'
                ),
                Column('estado', css_class='col-6 col-lg-3'),
            ),
            Row(
                Column('empleado', css_class='col-6 col-lg-3'),
                Column('cajero', css_class='col-6 col-lg-3'),
                Column('despachador', css_class='col-6 col-lg-3'),
                # Column(
                #     Field('orden_fechas',
                #           template="forms/fields/range-filter.html", css_class="form-control"),
                #     css_class='col-12 col-lg-6'
                # ),
                # Column(
                #     Field('orden_monto',
                #           template="forms/fields/range-filter.html", css_class="form-control", placeholder="$"),
                #     css_class='col-12 col-lg-6'
                # ),
                # Column(
                #     Field('orden_cantidad',
                #           template="forms/fields/range-filter.html", css_class="form-control"),
                #     css_class='col-12 col-lg-3'
                # ),
                # Column(
                #     Field('monto_credito', template="forms/fields/range-filter.html",
                #           css_class="form-control", placeholder="$"),
                #     css_class='col-lg-3 col-6'
                # ),
                Column(
                    StrictButton("Buscar", type='submit',
                                 css_class='btn btn-primary mt-1'),
                    css_class='col-12'
                )
            ),
        )
