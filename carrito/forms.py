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
