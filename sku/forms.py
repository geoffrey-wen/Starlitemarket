from django import forms
from .models import Product


class ProductInboundForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['exp_date','location']
