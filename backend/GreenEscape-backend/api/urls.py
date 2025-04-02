from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
 # Rediriger vers une page de succès après l'inscription
    path('', views.play_screen),
    path('generate_maze', views.generate_maze_view),

]
