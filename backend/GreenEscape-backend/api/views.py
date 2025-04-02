from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Bienvenue sur l'API Django avec MongoDB !"})

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../algorithms'))
import algo

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
