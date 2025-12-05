from django.urls import path
from .views import prueba

urlpatterns = [
    path('', prueba),
]
