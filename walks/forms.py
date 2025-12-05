from django import forms
from .models import Walk

class RatingForm(forms.Form):
    """Formulario para calificar un paseo"""
    rating = forms.IntegerField(
        label='Calificación (1-5)',
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5})
    )