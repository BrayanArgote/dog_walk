from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pet
from .forms import PetForm
from users.models import User

def listar_mascotas(request):
    """Listar todas las mascotas del propietario logueado"""
    # Verificar que esté logueado
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    # Verificar que sea propietario
    user_role = request.session.get('user_role')
    if user_role != 'owner':
        messages.error(request, 'Solo los propietarios pueden gestionar mascotas')
        return redirect('home')
    
    # Obtener mascotas del propietario
    mascotas = Pet.objects.filter(owner_id=user_id)
    
    return render(request, 'pets/listar.html', {'mascotas': mascotas})


def crear_mascota(request):
    """Crear una nueva mascota"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    if request.method == 'POST':
        formulario = PetForm(request.POST)
        if formulario.is_valid():
            mascota = formulario.save(commit=False)
            mascota.owner_id = user_id  # Asignar propietario
            mascota.save()
            messages.success(request, f'Mascota "{mascota.name}" creada exitosamente')
            return redirect('listar_mascotas')
    else:
        formulario = PetForm()
    
    return render(request, 'pets/crear.html', {'form': formulario})


def editar_mascota(request, pet_id):
    """Editar una mascota existente"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    # Obtener mascota y verificar que pertenezca al usuario
    mascota = get_object_or_404(Pet, id=pet_id, owner_id=user_id)
    
    if request.method == 'POST':
        formulario = PetForm(request.POST, instance=mascota)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, f'Mascota "{mascota.name}" actualizada')
            return redirect('listar_mascotas')
    else:
        formulario = PetForm(instance=mascota)
    
    return render(request, 'pets/editar.html', {'form': formulario, 'mascota': mascota})


def eliminar_mascota(request, pet_id):
    """Eliminar una mascota"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    mascota = get_object_or_404(Pet, id=pet_id, owner_id=user_id)
    
    if request.method == 'POST':
        nombre = mascota.name
        mascota.delete()
        messages.success(request, f'Mascota "{nombre}" eliminada')
        return redirect('listar_mascotas')
    
    return render(request, 'pets/eliminar.html', {'mascota': mascota})