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
    if not request.user.is_authenticated:
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
    else:
        return redirect('/')

@csrf_exempt
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                data = json.loads(request.body)  # Récupérer JSON envoyé
                username = data.get("username")
                password = data.get("password")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Requête invalide"}, status=400)

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login réussi!"}, status=200)
            else:
                return JsonResponse({"error": "Nom d'utilisateur ou mot de passe incorrect"}, status=400)

        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    else:
            return redirect('/')
    
@csrf_exempt
def saveBestTime(request):
    PlayerTimePerSeed = None
    if not request.user.is_authenticated:
        return redirect('login-page/')

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            seed = data.get("seed")
            playerTime = data.get("elapsed")
            playerId = request.user.id  # Utilisez request.user pour obtenir l'utilisateur actuel

            if seed is None or playerTime is None:
                return HttpResponseBadRequest("Données manquantes")

            # Enregistrez ou mettez à jour le meilleur temps pour le joueur et la graine
            player_time, created = PlayerTimePerSeed.objects.update_or_create(
                player_id=playerId,
                seed=seed,
                defaults={'time_played': playerTime}
            )

            return JsonResponse({"status": "succès", "created": created})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide"}, status=400)

    return HttpResponseBadRequest("Méthode non autorisée")


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('./login-page/')


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



def play_screen(request):
    if request.user.is_authenticated:
        print('authentifié')
        return render(request,'views/index.html')
        # user is not authenticated, redirect to login
    else:
        return redirect('/api/login-page/')

def register_page(request):
    if not request.user.is_authenticated:
        return render(request, "views/register.html")
    else:
        return redirect("/")

def login_page(request):
    if not request.user.is_authenticated:  
        return render(request, "views/login.html")
    else:
        return redirect("/")


from django.http import JsonResponse

def check_session(request):
    return JsonResponse({
        "session_key": request.session.session_key,
        "is_authenticated": request.user.is_authenticated,
        "user": str(request.user.id),
        "win": request.user.email,
    })


def auth_page(request):
    return render(request, 'views/authpage.html')

def profile(request):
    return render(request, "views/profile.html")

def retieveUserData(request):
    users = User.objects.all().values()  # Filtre les champs
    print("username : " , users[request.user.id-1])
    return JsonResponse(users[request.user.id-1])  # Retourne la liste au format JSON

def showScoreboard(request):
    return render(request, "views/scoreboard.html")