from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Ruta de registro
    path('login/', views.login_view, name='login'),      # Ruta de login
    path('logout/', views.logout_view, name='logout'),   # Ruta de logout
    path('', views.home, name='home'),
]