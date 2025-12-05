from django import forms
from .models import Ad
from pets.models import Pet

class AdForm(forms.ModelForm):
    """Formulario para crear/editar anuncios"""
    
    class Meta:
        model = Ad
        fields = ['pet', 'date', 'time', 'duration', 'place', 'text']
        labels = {
            'pet': 'Mascota',
            'date': 'Fecha del paseo',
            'time': 'Hora del paseo',
            'duration': 'Duración (minutos)',
            'place': 'Lugar',
            'text': 'Descripción (opcional)',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'text': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, user_id, *args, **kwargs):
        """Filtrar solo las mascotas del propietario logueado"""
        super().__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.filter(owner_id=user_id)