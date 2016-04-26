# -*- encoding: utf-8 -*-
from django import forms
from .models import Receipt
from datetimewidget.widgets import DateWidget


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ("product", "quantity", "date_expiration")
        widgets = {
            # Use localization and bootstrap 3
            'date_expiration': DateWidget(attrs={'id': "date_expiration"}, usel10n=True, bootstrap_version=3)
        }

    """def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Añadir atributos personalizados a campos sueltos.
        self.fields['date_expiration'].widget.attrs.update({'placeholder': 'Fecha en que caduca'})"""
