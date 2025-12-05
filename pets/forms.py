from django import forms
from .models import Pet

class PetForm(forms.ModelForm):
    """Formulario para crear/editar mascotas"""
    
    class Meta:
        model = Pet
        fields = ['name', 'type', 'image_url', 'notes']
        labels = {
            'name': 'Nombre',
            'type': 'Tipo de mascota',
            'image_url': 'URL de imagen (opcional)',
            'notes': 'Notas adicionales (opcional)',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }