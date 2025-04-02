from rest_framework import generics
from api.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User

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
