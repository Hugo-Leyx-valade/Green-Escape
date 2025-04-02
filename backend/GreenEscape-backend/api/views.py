from rest_framework import generics
from api.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User
from api.algorithms import algo

def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API Green Escape"})


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Hacher le mot de passe
        hashed_password = make_password(password)

        # Créer et enregistrer l'utilisateur
        new_user = User(username=username, email=email, password=hashed_password)
        new_user.save()

    return render(request, 'register.html')  # Page d'inscription


def generate_maze_view(request):
    seed = request.GET.get('seed')
    if not seed:
        return JsonResponse({'error': 'Missing seed'}, status=400)
    
    try:
        seed = int(seed)
    except ValueError:
        return JsonResponse({'error': 'Invalid seed'}, status=400)

    result = algo.generate_maze(seed)
    return JsonResponse(result)


def play_screen(request):
    return render(request,'views/index.html')