from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('api/', include("django.contrib.auth.urls")),
    path('generate_maze', views.generate_maze_view),
     # Authentification Django
    path('accounts/', include('django.contrib.auth.urls')),
]
