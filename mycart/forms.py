from dataclasses import field
from django import forms
from .models import Coupons

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = ['code']

        # def __init__(self, *args, **kwargs):
        #    super().__init__(*args, **kwargs)
        #    self.fields['code'].widget.attrs.update({'class': 'form-control'})
