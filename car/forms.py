from django import forms
from .models import Car


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['owner_number', 'images', 'name', 'model', 'generation', 'year', 'transmission_type',
                  'description', 'colour', 'doors', 'fuel_type', 'price', 'sale_type']