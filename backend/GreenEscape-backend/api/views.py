from rest_framework import generics
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from .models import PlayerTimePerSeed
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
from django.http import JsonResponse, HttpResponseBadRequest


sys.path.append(os.path.join(os.path.dirname(__file__), '../../../algorithms'))

def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API Green Escape"})

User = get_user_model()
CustomUser = get_user_model()


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
def saveBestTime(request, seed):
    if not request.user.is_authenticated:
        return redirect('login-page/')

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            playerTime = data.get("elapsed")
            playerId = request.user.id

            print("Données reçues dans saveBestTime :", {"seed": seed, "playerTime": playerTime, "playerId": playerId})

            if playerTime is None:
                return HttpResponseBadRequest("Données manquantes")

            # Vérifie s'il existe déjà un enregistrement pour ce joueur et cette graine
            try:
                player_time = PlayerTimePerSeed.objects.get(player_id=playerId, seed=seed)

                if player_time.time_played is None or playerTime < player_time.time_played:
                    player_time.time_played = playerTime
                    player_time.save()
                    print("Temps mis à jour :", {"nouveau_temps": playerTime})
                    return JsonResponse({"status": "succès", "updated": True})
                else:
                    print("Temps non mis à jour : temps existant meilleur ou égal")
                    return JsonResponse({"status": "succès", "updated": False, "reason": "existing time is better or equal"})

            except PlayerTimePerSeed.DoesNotExist:
                # Aucun temps existant, on en crée un nouveau
                PlayerTimePerSeed.objects.create(
                    player_id=playerId,
                    seed=seed,
                    time_played=playerTime
                )
                print("Nouveau temps enregistré :", {"playerId": playerId, "seed": seed, "time": playerTime})
                return JsonResponse({"status": "succès", "created": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Requête invalide"}, status=400)

    return HttpResponseBadRequest("Méthode non autorisée")



from django.contrib.auth import logout

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
        return redirect('/api/hub/')
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
    try:
        # Récupérer l'utilisateur actuel
        user = User.objects.get(id=request.user.id)
        
        # Préparer les données utilisateur
        user_data = {
            "id": user.id,
            "password": user.password,
            "last_login": user.last_login,
            "is_superuser": user.is_superuser,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_active": user.is_active,
            "date_joined": user.date_joined,
            "played_game": getattr(user, "played_game", 0),  # Assurez-vous que ce champ existe dans le modèle
            "medails": getattr(user, "medails", 0),  # Assurez-vous que ce champ existe dans le modèle
        }
        
        # Retourner les données utilisateur sous forme de JSON
        return JsonResponse(user_data, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "Utilisateur non trouvé"}, status=404)

def showScoreboard(request):
    return render(request, "views/scoreboard.html")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def saveMedals(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Utilisateur non authentifié"}, status=401)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            medals = data.get('medals')
            print("medals:", medals)
            playerId = request.user.id

            if playerId and medals is not None:
                User.objects.update_or_create(
                    id=playerId,
                    defaults={'medails': medals}  # ⚠️ assure-toi que "medails" est le bon champ
                )
                return JsonResponse({"message": "Médailles sauvegardées avec succès"}, status=201)
            else:
                return JsonResponse({"error": "ID utilisateur ou médailles manquantes"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Format JSON invalide"}, status=400)

    return JsonResponse({"error": "Méthode non autorisée"}, status=405)
  
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

@csrf_exempt
@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        response_data = {}

        # Vérifiez si un nouveau username est fourni
        if "username" in request.POST:
            new_username = request.POST["username"]
            # Vérifiez si le username existe déjà
            if CustomUser.objects.filter(username=new_username).exclude(id=user.id).exists():
                return JsonResponse({"error": "Username already exists."}, status=400)
            user.username = new_username
            response_data["username"] = new_username

        # Vérifiez si un nouveau mot de passe est fourni
        if "newPassword" in request.POST:
            new_password = request.POST["newPassword"]
            user.set_password(new_password)
            response_data["password"] = "Password updated."

        # Sauvegardez les modifications uniquement si des changements ont été effectués
        if response_data:
            user.save()
            return JsonResponse({"message": "Profile updated successfully!", "data": response_data})

        return JsonResponse({"error": "No changes were made."}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

def scoreboard(request):
    # Récupérer les 10 joueurs avec le plus de médailles, triés par médailles (descendant) et username (ascendant)
    top_players = CustomUser.objects.all().order_by('-medails', 'username')[:10]
    return render(request, "views/scoreboard.html", {"top_players": top_players})

def hub(request):
    if request.user.is_authenticated:
        return render(request, "views/index.html")
    else:
        return redirect('/api/login-page/')

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Déconnexion réussie"}, status=200)
    return JsonResponse({"error": "Méthode non autorisée"}, status=405)

@csrf_exempt
@login_required
def update_player_stats(request):
    if request.method == "POST":
        try:
            user = request.user
            data = json.loads(request.body)
            medails_to_add = data.get("medails", 0)
            user.medails += medails_to_add
            user.played_game += 1
            user.save()
            return JsonResponse({"message": "Stats updated successfully!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

from django.db.models import Min

from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def scoreboard_by_seed(request):
    seed = request.GET.get('seed')
    if not seed:
        return JsonResponse({"error": "Missing seed"}, status=400)

    try:
        seed = int(seed)
    except ValueError:
        return JsonResponse({"error": "Invalid seed"}, status=400)

    # Récupérer les 10 meilleurs joueurs par temps pour la graine donnée
    top_players = PlayerTimePerSeed.objects.filter(seed=seed).order_by('time_played')[:10]
    players_data = []

    for player_time in top_players:
        try:
            user = User.objects.get(id=player_time.player_id)  # Récupérer l'utilisateur à partir de l'ID
            players_data.append({
                "username": user.username,
                "time_played": player_time.time_played,
            })
        except User.DoesNotExist:
            players_data.append({
                "username": f"Unknown (ID: {player_time.player_id})",
                "time_played": player_time.time_played,
            })

    return JsonResponse({"seed": seed, "top_players": players_data}, status=200)
