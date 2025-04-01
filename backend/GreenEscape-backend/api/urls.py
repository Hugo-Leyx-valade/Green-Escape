from django.urls import path
from .views import home

urlpatterns = [
    path('', home),  # Route principale de l'API
]