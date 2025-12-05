from django.urls import path
from . import views

urlpatterns = [
    # Rutas para propietarios
    path('mis-anuncios/', views.listar_mis_anuncios, name='listar_mis_anuncios'),
    path('crear/', views.crear_anuncio, name='crear_anuncio'),
    path('editar/<int:ad_id>/', views.editar_anuncio, name='editar_anuncio'),
    path('cerrar/<int:ad_id>/', views.cerrar_anuncio, name='cerrar_anuncio'),
    
    # Rutas para paseadores
    path('disponibles/', views.listar_anuncios_disponibles, name='listar_anuncios_disponibles'),
    path('detalle/<int:ad_id>/', views.detalle_anuncio, name='detalle_anuncio'),
]