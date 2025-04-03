from rest_framework import generics
from api.models import User
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import User
from api.algorithms import algo
from api.algorithms import solvers

from django.contrib.auth.forms import AuthenticationForm


import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../algorithms'))


def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API Green Escape"})


from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


from django.contrib.auth import logout

def logout_view(request):
        logout(request)
        # clear the user's session data
        Session.objects.filter(session_key=request.session.session_key).delete()
        return redirect('home')

def generate_maze_view(request):
    if request.user.is_authenticated:

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
    else:
        # user is not authenticated, redirect to login
        return redirect('/login/')

def play_screen(request):
    if request.user.is_authenticated:
        return render(request,'views/index.html')
    else:
        # user is not authenticated, redirect to login
        return redirect('login/')

   