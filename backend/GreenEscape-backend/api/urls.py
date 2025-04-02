from django.urls import path
from .views import home
from . import views


urlpatterns = [
    path('', views.home),
    path('generate_maze', views.generate_maze_view),
]