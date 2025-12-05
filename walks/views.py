from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Request, Walk
from .forms import RatingForm
from ads.models import Ad

# ==================== SOLICITUDES ====================

def enviar_solicitud(request, ad_id):
    """Paseador envía solicitud a un anuncio"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'walker':
        messages.error(request, 'Solo los paseadores pueden enviar solicitudes')
        return redirect('home')
    
    anuncio = get_object_or_404(Ad, id=ad_id, status='available')
    
    # Verificar si ya envió solicitud a este anuncio
    solicitud_existente = Request.objects.filter(ad=anuncio, walker_id=user_id).exists()
    if solicitud_existente:
        messages.warning(request, 'Ya enviaste una solicitud a este anuncio')
        return redirect('detalle_anuncio', ad_id=ad_id)
    
    if request.method == 'POST':
        # Crear solicitud con estado pendiente
        Request.objects.create(
            ad=anuncio,
            walker_id=user_id,
            status='pending'
        )
        messages.success(request, 'Solicitud enviada exitosamente')
        return redirect('mis_solicitudes')
    
    return render(request, 'walks/enviar_solicitud.html', {'anuncio': anuncio})


def mis_solicitudes(request):
    """Paseador ve sus solicitudes enviadas"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    solicitudes = Request.objects.filter(walker_id=user_id).select_related('ad', 'ad__pet')
    
    return render(request, 'walks/mis_solicitudes.html', {'solicitudes': solicitudes})


def solicitudes_recibidas(request):
    """Propietario ve solicitudes a sus anuncios"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'owner':
        messages.error(request, 'Solo los propietarios pueden ver solicitudes')
        return redirect('home')
    
    # Obtener solicitudes de anuncios de sus mascotas
    solicitudes = Request.objects.filter(
        ad__pet__owner_id=user_id
    ).select_related('ad', 'ad__pet', 'walker')
    
    return render(request, 'walks/solicitudes_recibidas.html', {'solicitudes': solicitudes})


def aceptar_solicitud(request, request_id):
    """Propietario acepta una solicitud - crea un paseo"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    solicitud = get_object_or_404(
        Request, 
        id=request_id, 
        ad__pet__owner_id=user_id,
        status='pending'
    )
    
    if request.method == 'POST':
        # Cambiar estado de solicitud
        solicitud.status = 'accepted'
        solicitud.save()
        
        # Crear paseo
        Walk.objects.create(
            ad=solicitud.ad,
            walker_id=solicitud.walker.id,
            status='pending'
        )
        
        # Cerrar el anuncio
        solicitud.ad.status = 'not_available'
        solicitud.ad.save()
        
        # Rechazar otras solicitudes pendientes del mismo anuncio
        Request.objects.filter(ad=solicitud.ad, status='pending').exclude(id=request_id).update(status='rejected')
        
        messages.success(request, 'Solicitud aceptada. Paseo creado.')
        return redirect('solicitudes_recibidas')
    
    return render(request, 'walks/aceptar_solicitud.html', {'solicitud': solicitud})


def rechazar_solicitud(request, request_id):
    """Propietario rechaza una solicitud"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    solicitud = get_object_or_404(
        Request, 
        id=request_id, 
        ad__pet__owner_id=user_id,
        status='pending'
    )
    
    if request.method == 'POST':
        solicitud.status = 'rejected'
        solicitud.save()
        messages.success(request, 'Solicitud rechazada')
        return redirect('solicitudes_recibidas')
    
    return render(request, 'walks/rechazar_solicitud.html', {'solicitud': solicitud})


# ==================== PASEOS ====================

def mis_paseos(request):
    """Paseador ve sus paseos"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'walker':
        messages.error(request, 'Solo los paseadores pueden ver sus paseos')
        return redirect('home')
    
    paseos = Walk.objects.filter(walker_id=user_id).select_related('ad', 'ad__pet')
    
    return render(request, 'walks/mis_paseos.html', {'paseos': paseos})


def paseos_propietario(request):
    """Propietario ve paseos de sus mascotas"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    if user_role != 'owner':
        messages.error(request, 'Solo los propietarios pueden ver paseos')
        return redirect('home')
    
    paseos = Walk.objects.filter(
        ad__pet__owner_id=user_id
    ).select_related('ad', 'ad__pet', 'walker')
    
    return render(request, 'walks/paseos_propietario.html', {'paseos': paseos})


def iniciar_paseo(request, walk_id):
    """Paseador inicia el paseo"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    paseo = get_object_or_404(Walk, id=walk_id, walker_id=user_id, status='pending')
    
    if request.method == 'POST':
        paseo.status = 'in_progress'
        paseo.start_time = timezone.now()
        paseo.save()
        messages.success(request, 'Paseo iniciado')
        return redirect('mis_paseos')
    
    return render(request, 'walks/iniciar_paseo.html', {'paseo': paseo})


def finalizar_paseo(request, walk_id):
    """Paseador finaliza el paseo"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    paseo = get_object_or_404(Walk, id=walk_id, walker_id=user_id, status='in_progress')
    
    if request.method == 'POST':
        paseo.status = 'done'
        paseo.end_time = timezone.now()
        paseo.save()
        messages.success(request, 'Paseo finalizado. Esperando calificación del propietario.')
        return redirect('mis_paseos')
    
    return render(request, 'walks/finalizar_paseo.html', {'paseo': paseo})


def calificar_paseo(request, walk_id):
    """Propietario califica el paseo"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    paseo = get_object_or_404(Walk, id=walk_id, ad__pet__owner_id=user_id, status='done')
    
    # Verificar que no esté calificado
    if paseo.rating is not None:
        messages.warning(request, 'Este paseo ya fue calificado')
        return redirect('paseos_propietario')
    
    if request.method == 'POST':
        formulario = RatingForm(request.POST)
        if formulario.is_valid():
            paseo.rating = formulario.cleaned_data['rating']
            paseo.save()
            messages.success(request, f'Paseo calificado con {paseo.rating} estrellas')
            return redirect('paseos_propietario')
    else:
        formulario = RatingForm()
    
    return render(request, 'walks/calificar_paseo.html', {'form': formulario, 'paseo': paseo})


def cancelar_paseo(request, walk_id):
    """Cancelar un paseo (propietario o paseador)"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Debes iniciar sesión')
        return redirect('login')
    
    user_role = request.session.get('user_role')
    
    # Verificar permisos según rol
    if user_role == 'walker':
        paseo = get_object_or_404(Walk, id=walk_id, walker_id=user_id)
    else:
        paseo = get_object_or_404(Walk, id=walk_id, ad__pet__owner_id=user_id)
    
    # Solo se puede cancelar si está pendiente (NO en progreso)
    if paseo.status != 'pending':
        messages.error(request, 'No se puede cancelar este paseo')
        if user_role == 'walker':
            return redirect('mis_paseos')
        else:
            return redirect('paseos_propietario')
    
    if request.method == 'POST':
        paseo.status = 'canceled'
        paseo.save()
        messages.success(request, 'Paseo cancelado')
        
        if user_role == 'walker':
            return redirect('mis_paseos')
        else:
            return redirect('paseos_propietario')
    
    return render(request, 'walks/cancelar_paseo.html', {'paseo': paseo})