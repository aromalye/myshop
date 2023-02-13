from .models import Order
from django import forms


class AddChoice(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {'status' : forms.MultipleChoiceField(choices=Order.STATUS)}

