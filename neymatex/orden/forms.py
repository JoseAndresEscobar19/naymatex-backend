from django import forms
from django.db.models import fields
from neymatex.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_forms.bootstrap import PrependedText


class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = "__all__"
        labels = {
            "codigo": "Código",
            "estado": 'Estado del Pedido',
        }
        widgets = {
            "codigo": forms.HiddenInput(),
            # "fecha": forms.TextInput(),
            # "cliente": forms.Select(),
            # "empleado": forms.Select(),
            # "subtotal": forms.HiddenInput(),
            # "iva": forms.HiddenInput(),
            # "descuento": forms.HiddenInput(),
            # "valor_total": forms.HiddenInput(),
            "estado": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                'codigo',
                'estado',
                Column('cliente', css_class='col-12 col-lg-4'),
                Column('empleado', css_class='col-12 col-lg-4'),
                Column('fecha', css_class='col-12 col-lg-4'),
                Column('subtotal', css_class='col-12 col-lg-4'),
                Column('iva', css_class='col-12 col-lg-4'),
                Column('descuento', css_class='col-12 col-lg-4'),
                Column('valor_total', css_class='col-12 col-lg-4'),
            ),
            # Row(
            #     Column('unidad', css_class='col-12 col-lg-4'),
            #     Column('cantidad', css_class='col-12 col-lg-4'),
            #     Column(PrependedText('precio', '$'),
            #            css_class='col-12 col-lg-4'),
            #     Column('imagen', css_class='col-12 col-lg-8'),
            # ),
        )
