from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User

def register(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        formulario = RegisterForm(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            # Guardar contraseña (después usaremos hash)
            usuario.password = formulario.cleaned_data['password']
            usuario.save()
            messages.success(request, 'Usuario registrado exitosamente')
            return redirect('login')
    else:
        formulario = RegisterForm()
    
    return render(request, 'users/register.html', {'form': formulario})


def login_view(request):
    """Vista de inicio de sesión"""
    if request.method == 'POST':
        formulario = LoginForm(request.POST)
        if formulario.is_valid():
            email = formulario.cleaned_data['email']
            password = formulario.cleaned_data['password']
            
            try:
                usuario = User.objects.get(email=email, password=password)
                # Guardar datos en sesión
                request.session['user_id'] = usuario.id
                request.session['user_role'] = usuario.role
                messages.success(request, f'Bienvenido {usuario.first_name}')
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, 'Email o contraseña incorrectos')
    else:
        formulario = LoginForm()
    
    return render(request, 'users/login.html', {'form': formulario})


def logout_view(request):
    """Cerrar sesión"""
    request.session.flush()  # Elimina todos los datos de sesión
    messages.success(request, 'Sesión cerrada correctamente')
    return redirect('login')

def home(request):
    """Vista de página principal"""
    return render(request, 'users/home.html')