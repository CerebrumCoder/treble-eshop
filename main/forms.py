from django.forms import ModelForm
from main.models import Product
# from django import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "rating", "stock", "description", "thumbnail"]

# class CarForm(forms.Form):
#     name = forms.CharField(max_length=255)
#     brand = forms.CharField(max_length=255)
#     stock = forms.IntegerField(default=0)