# -*- encoding: utf-8 -*-
from django import forms
from .models import Receipt, Send, Sale, DetailSend, TYPE_RECEIPT, DetailSale
from datetimewidget.widgets import DateWidget
from django.utils import timezone


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ("product", "quantity", "date_expiration", "no_lote", "distribuidor", "factura")
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

    def clean_product(self):
        product = self.cleaned_data.get('product', None)
        if product is None:
            raise forms.ValidationError("Se debe de seleccionar un producto para recibir")
        return product

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity', 0)
        if quantity == 0:
            raise forms.ValidationError("El valor de cantidad debe de ser mayor a 0")
        return quantity

    def clean_date_expiration(self):
        date_expiration = self.cleaned_data.get("date_expiration", None)
        now = timezone.localtime(timezone.now())
        if date_expiration is None:
            raise forms.ValidationError("Se debe de ingresar una fecha de caducidad")
            return date_expiration
        if date_expiration <= now.date():
            raise forms.ValidationError("La fecha de caducidad debe der mayor al dia de hoy")
        return date_expiration

    def clean_no_lote(self):
        no_lote = self.cleaned_data.get('no_lote', '')
        if len(no_lote) == 0:
            raise forms.ValidationError("Falta el numero de lote")
        return no_lote

    def clean_distribuidor(self):
        distribuidor = self.cleaned_data.get('distribuidor', '')
        if len(distribuidor) <= 3:
            raise forms.ValidationError("Falta el distribuidor")
        return distribuidor

    def clean_factura(self):
        factura = self.cleaned_data.get('factura', '')
        if len(factura) <= 3:
            raise forms.ValidationError("Falta la factura")
        return factura


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

    def clean_sale(self):
        sale = self.cleaned_data.get('sale', None)
        if sale is None:
            raise forms.ValidationError("Se debe de seleccionar una venta para el envio")
        return sale


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

    def clean_send(self):
        send = self.cleaned_data.get('send', None)
        if send is None:
            raise forms.ValidationError("Se debe de seleccionar una venta para el envio")
        return send

    def clean_detail_sale(self):
        detail_sale = self.cleaned_data.get('detail_sale', None)
        if detail_sale is None:
            raise forms.ValidationError("Se debe de seleccionar una linea del pedido")
        return detail_sale

    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt', None)
        if receipt is None:
            raise forms.ValidationError("Se debe de seleccionar un recibo para asociar")
            return receipt
        if receipt.quantity <= 0:
            raise forms.ValidationError("Solo se puede seleccionar recibos con inventario activo")
        return receipt

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity', 0)
        if quantity == 0:
            raise forms.ValidationError("El valor de cantidad debe de ser mayor a 0")
        return quantity
