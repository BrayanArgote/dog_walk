from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Ad
from .forms import AdForm
from pets.models import Pet

def listar_mis_anuncios(request):
    """Listar anuncios del propietario logueado"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'owner':
        messages.error(request, 'Solo los propietarios pueden gestionar anuncios')
        return redirect('home')
    
    # Obtener anuncios de mascotas del propietario
    mis_mascotas = Pet.objects.filter(owner_id=user_id)
    anuncios = Ad.objects.filter(pet__in=mis_mascotas)
    
    return render(request, 'ads/mis_anuncios.html', {'anuncios': anuncios})


def crear_anuncio(request):
    """Crear un nuevo anuncio"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    # Verificar que tenga mascotas
    tiene_mascotas = Pet.objects.filter(owner_id=user_id).exists()
    if not tiene_mascotas:
        messages.error(request, 'Debes registrar al menos una mascota primero')
        return redirect('crear_mascota')
    
    if request.method == 'POST':
        formulario = AdForm(user_id, request.POST)
        if formulario.is_valid():
            anuncio = formulario.save(commit=False)
            anuncio.status = 'available'  # Por defecto disponible
            anuncio.save()
            messages.success(request, 'Anuncio creado exitosamente')
            return redirect('listar_mis_anuncios')
    else:
        formulario = AdForm(user_id)
    
    return render(request, 'ads/crear.html', {'form': formulario})


def editar_anuncio(request, ad_id):
    """Editar un anuncio existente"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    # Verificar que el anuncio pertenezca a una mascota del usuario
    anuncio = get_object_or_404(Ad, id=ad_id, pet__owner_id=user_id)
    
    if request.method == 'POST':
        formulario = AdForm(user_id, request.POST, instance=anuncio)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Anuncio actualizado')
            return redirect('listar_mis_anuncios')
    else:
        formulario = AdForm(user_id, instance=anuncio)
    
    return render(request, 'ads/editar.html', {'form': formulario, 'anuncio': anuncio})


def cerrar_anuncio(request, ad_id):
    """Cambiar estado del anuncio a 'not_available'"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    anuncio = get_object_or_404(Ad, id=ad_id, pet__owner_id=user_id)
    
    if request.method == 'POST':
        anuncio.status = 'not_available'
        anuncio.save()
        messages.success(request, 'Anuncio cerrado')
        return redirect('listar_mis_anuncios')
    
    return render(request, 'ads/cerrar.html', {'anuncio': anuncio})


def listar_anuncios_disponibles(request):
    """Listar anuncios disponibles para paseadores"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'walker':
        messages.error(request, 'Solo los paseadores pueden ver anuncios disponibles')
        return redirect('home')
    
    # Solo anuncios con status 'available'
    anuncios = Ad.objects.filter(status='available').select_related('pet', 'pet__owner')
    
    return render(request, 'ads/disponibles.html', {'anuncios': anuncios})

def detalle_anuncio(request, ad_id):
    """Ver detalle de un anuncio"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    anuncio = get_object_or_404(Ad, id=ad_id)
    
    # Verificar si el walker tiene solicitud aceptada
    mostrar_contacto = True
    if request.session.get('user_role') == 'walker':
        from walks.models import Request
        solicitud = Request.objects.filter(
            ad=anuncio, 
            walker_id=user_id, 
            status='accepted'
        ).first()
        mostrar_contacto = solicitud is not None
    
    return render(request, 'ads/detalle.html', {
        'anuncio': anuncio,
        'mostrar_contacto': mostrar_contacto
    })