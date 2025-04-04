from rest_framework import generics
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from api.algorithms import algo
from api.algorithms import solvers
from django.contrib.auth.forms import AuthenticationForm
import sys, os
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../algorithms'))

def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API Green Escape"})

User = get_user_model()


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            if not username or not password:
                return JsonResponse({"error": "Missing fields"}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already taken"}, status=400)
            user = User.objects.create(username=username, password=make_password(password))
            return JsonResponse({"message": "User created successfully"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)  # Gérer les requêtes non POST


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        # Récupération des données envoyées
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authentifier l'utilisateur
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login réussi!"}, status=200)
        else:
            return JsonResponse({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)



def logout_view(request):
        logout(request)
        # clear the user's session data
        Session.objects.filter(session_key=request.session.session_key).delete()
        return redirect('home')

@login_required(login_url="/login/")
def generate_maze_view(request):
        seed = request.GET.get('seed')
        if not seed:
            return JsonResponse({'error': 'Missing seed'}, status=400)      
        try:
            seed = int(seed)
        except ValueError:
            return JsonResponse({'error': 'Invalid seed'}, status=400)
        result = algo.generate_maze(seed)
        maze = result["maze"]
        start = tuple(result["entrance"])
        goal = tuple(result["exit"])
        scores = {
            "A*": solvers.solve_with_astar(maze, start, goal),
            "Dijkstra": solvers.solve_with_dijkstra(maze, start, goal),
            "BFS": solvers.solve_with_bfs(maze, start, goal),
        }
        sorted_scores = sorted(scores.items(), key=lambda x: x[1])
        result["scores"] = sorted_scores
        return JsonResponse(result)


@login_required(login_url="/login/")
def play_screen(request):
        return render(request,'views/index.html')
        # user is not authenticated, redirect to login

def register_page(request):
    return render(request, "views/register.html")

def login_page(request):
     return render(request, "views/login.html")