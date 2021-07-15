from django import forms
from django.db.models import fields
from neymatex.models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div
from crispy_forms.bootstrap import PrependedText


class NotificacionForm(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'
        labels = {
            "title": "Título",
            "body": "Mensaje",
            "imagen": "Imagen",
            "grupo_usuarios": "Grupo de usuarios a quienes enviar:"
        }
        widgets = {
            # "codigo": forms.HiddenInput(),
            # "estado": forms.HiddenInput(),
            # "is_active": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

        # self.helper.layout = Layout(
        #     Row(
        #         Div(
        #             'codigo',
        #             'estado',
        #             'is_active',
        #         ),
        #         Column(
        #             PrependedText('monto_credito', '$',
        #                           placeholder=""),
        #             css_class='col-lg-4 col-6'
        #         ),
        #     ),
        # )


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
