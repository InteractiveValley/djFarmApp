# -*- encoding: utf-8 -*-
from django import forms
from .models import Receipt, Send, Sale, DetailSend, TYPE_RECEIPT, DetailSale
from datetimewidget.widgets import DateWidget


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ("product", "quantity", "date_expiration")
        widgets = {
            # Use localization and bootstrap 3
            'date_expiration': DateWidget(attrs={'id': "date_expiration"}, usel10n=True, bootstrap_version=3)
        }

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # Añadir atributos personalizados a campos sueltos.
        self.fields['date_expiration'].widget.attrs.update({'placeholder': 'Fecha en que caduca'})


class SendForm(forms.ModelForm):
    class Meta:
        model = Send
        fields = ("sale",)

    def __init__(self, *args, **kwargs):
        super(SendForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        sale_list = Sale.objects.filter(with_shipping=False)

        self.fields['sale'].queryset = sale_list


class DetailSendForm(forms.ModelForm):
    class Meta:
        model = DetailSend
        fields = ("send", "detail_sale", "receipt", "quantity")

    def __init__(self, *args, **kwargs):
        detalle_envio = kwargs.pop('detalle_envio', None)

        super(DetailSendForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            # Recorremos todos los campos del modelo para añadirle class="form-control
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        if detalle_envio:
            self.fields['send'].queryset = Send.objects.filter(sale=detalle_envio[0]['send'].sale)
            self.fields['send'].initial = detalle_envio[0]['send']
            self.fields['detail_sale'].queryset = DetailSale.objects.filter(sale=detalle_envio[0]['send'].sale)
            self.fields['detail_sale'].initial = detalle_envio[0]['detail_sale']
            self.fields['receipt'].queryset = Receipt.objects.filter(product=detalle_envio[0]['product'],
                                                                     type_receipt=TYPE_RECEIPT,
                                                                     quantity__gt=0)
            self.fields['receipt'].initial = detalle_envio[0]['product']