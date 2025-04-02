from django.shortcuts import render
from django.http import JsonResponse
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../algorithms'))

import algo
import solvers

def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API Django avec MongoDB !"})

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
