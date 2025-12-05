from django.urls import path
from . import views

urlpatterns = [
    # Solicitudes
    path('enviar-solicitud/<int:ad_id>/', views.enviar_solicitud, name='enviar_solicitud'),
    path('mis-solicitudes/', views.mis_solicitudes, name='mis_solicitudes'),
    path('solicitudes-recibidas/', views.solicitudes_recibidas, name='solicitudes_recibidas'),
    path('aceptar-solicitud/<int:request_id>/', views.aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar-solicitud/<int:request_id>/', views.rechazar_solicitud, name='rechazar_solicitud'),
    
    # Paseos
    path('mis-paseos/', views.mis_paseos, name='mis_paseos'),
    path('paseos-propietario/', views.paseos_propietario, name='paseos_propietario'),
    path('iniciar/<int:walk_id>/', views.iniciar_paseo, name='iniciar_paseo'),
    path('finalizar/<int:walk_id>/', views.finalizar_paseo, name='finalizar_paseo'),
    path('calificar/<int:walk_id>/', views.calificar_paseo, name='calificar_paseo'),
    path('cancelar/<int:walk_id>/', views.cancelar_paseo, name='cancelar_paseo'),
]