from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    """Formulario de registro de usuarios"""
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput, 
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
            'password': forms.PasswordInput(),
        }
    
    def clean(self):
        """Validar que las contraseñas coincidan"""
        datos_limpios = super().clean()
        password = datos_limpios.get('password')
        confirmar_password = datos_limpios.get('confirmar_password')
        
        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return datos_limpios


class LoginForm(forms.Form):
    """Formulario de inicio de sesión"""
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        label="Contraseña"
    )