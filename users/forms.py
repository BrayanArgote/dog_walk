from django import forms
from .models import User
import re

class RegisterForm(forms.ModelForm):
    """Formulario de registro de usuarios con validaciones"""
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'required': True,
            'minlength': '7'
        }), 
        label="Confirmar contraseña"
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'age', 'email', 'password', 'role', 'phone', 'address']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'age': 'Edad',
            'email': 'Correo electrónico',
            'password': 'Contraseña',
            'role': 'Rol',
            'phone': 'Teléfono',
            'address': 'Dirección',
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'required': True,
                'minlength': '7'
            }),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'age': forms.NumberInput(attrs={'required': True, 'min': '18'}),
            'email': forms.EmailInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={
                'required': True,
                'pattern': '[0-9]{10}',
                'maxlength': '10',
                'minlength': '10',
                'title': 'Ingresa un teléfono de 10 dígitos (solo números)'
            }),
            'address': forms.TextInput(attrs={'required': True}),
        }
    
    def clean_age(self):
        """Validar que la edad sea mayor o igual a 18"""
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise forms.ValidationError("Debes ser mayor de 18 años para registrarte")
        return age
    
    def clean_phone(self):
        """Validar que el teléfono tenga solo números y exactamente 10 dígitos"""
        phone = self.cleaned_data.get('phone')
        
        phone = phone.strip()

        if not phone.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números")
        
        if len(phone) != 10:
            raise forms.ValidationError("El teléfono debe tener exactamente 10 dígitos")
        
        return phone
    
    def clean_password(self):
        """Validar que la contraseña tenga al menos 7 caracteres, números y letras"""
        password = self.cleaned_data.get('password')
        
        if len(password) < 7:
            raise forms.ValidationError("La contraseña debe tener al menos 7 caracteres")
        
        if not re.search(r'\d', password):
            raise forms.ValidationError("La contraseña debe contener al menos un número")
        
        if not re.search(r'[a-zA-Z]', password):
            raise forms.ValidationError("La contraseña debe contener al menos una letra")
        
        return password
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        datos_limpios = super().clean()
        password = datos_limpios.get('password')
        confirmar_password = datos_limpios.get('confirmar_password')
        
        if password and confirmar_password and password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return datos_limpios


class LoginForm(forms.Form):
    """Formulario de inicio de sesión"""
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'required': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'required': True}), 
        label="Contraseña"
    )