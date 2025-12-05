from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_mascotas, name='listar_mascotas'),
    path('crear/', views.crear_mascota, name='crear_mascota'),
    path('editar/<int:pet_id>/', views.editar_mascota, name='editar_mascota'),
    path('eliminar/<int:pet_id>/', views.eliminar_mascota, name='eliminar_mascota'),
]