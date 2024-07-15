from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import viewsets
from bson import ObjectId
from .models import Game
from .serializers import GameSerializer
from django.apps import apps
from datetime import datetime
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf(request):
    csrf_token = get_token(request)
    print("CSRF_TOKEN:", csrf_token)
    return JsonResponse({'csrf_token': csrf_token})

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

# def get_game_by_id(request, id):
#     game = get_object_or_404(Game, _id=ObjectId(id))
#     serializer = GameSerializer(game)
#     return JsonResponse(serializer.data)

def get_title_by_id(id):
    game = get_object_or_404(Game, _id=ObjectId(id))
    serializer = GameSerializer(game)
    return serializer.data['title']

def start_game(request, id):
    app_config = apps.get_app_config('game')
    stopwatch = app_config.stopwatch

    if stopwatch.game_id is None or stopwatch.game_id == '':
        stopwatch.game_id = id
        stopwatch.game_title = get_title_by_id(id)
        stopwatch.start_time = datetime.now()
        stopwatch.end_time = ''
        stopwatch.duration = 0

        # return redirect('/game/')
        return JsonResponse({'message': 'OK'})
    else:
        return JsonResponse({'message': 'A game is already starting...'})

def stopwatch(request):
    app_cfg = apps.get_app_config('game')
    stopwatch = app_cfg.stopwatch
    return JsonResponse({
        'game_id': stopwatch.game_id,
        'game_title': stopwatch.game_title,
        'start_time': stopwatch.start_time,
        'end_time': stopwatch.end_time,
        'duration': stopwatch.duration,
    })

def stop_game(request):
    app_config = apps.get_app_config('game')
    stopwatch = app_config.stopwatch
    
    if stopwatch is not None:
        stopwatch.end_time = datetime.now()
        duration = stopwatch.end_time - stopwatch.start_time
        total_seconds = duration.total_seconds()
        stopwatch.duration = int(total_seconds // 60)

        try:
            game_id = ObjectId(stopwatch.game_id)
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return JsonResponse({'message': 'Game not found!'}, status=404)

        game.played_time += stopwatch.duration
        game.save()

        stopwatch.clear()
        return JsonResponse({'message': 'Ended!'})
    else:
        return JsonResponse({'message': 'No active game!'})

@api_view(['POST'])
def create_game(request):
    data = request.data.copy()
    data['played_time'] = 0
    data['time_to_beat'] = 0
    data['status'] = "Playing"

    serializer = GameSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return redirect('/game/')

def to_update_game(request, id):
    try:
        game_id = ObjectId(id)
    except Exception as e:
        return Response({"error": "Invalid game ID"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
            serializer = GameSerializer(game)
            return JsonResponse(serializer.data)

@csrf_protect
def update_game(request):
    try:
        game_id = ObjectId(request.POST.get('id'))
        game = Game.objects.get(pk=game_id)
        if request.method == 'POST':
            played_time_hour = int(request.POST.get('played_time_hour'), 0)
            played_time_min = int(request.POST.get('played_time_min'), 0)
            time_to_beat_hour = int(request.POST.get('time_to_beat_hour'), 0)
            time_to_beat_min = int(request.POST.get('time_to_beat_min'), 0)
            
            played_time = played_time_hour * 60 + played_time_min
            time_to_beat = time_to_beat_hour * 60 + time_to_beat_min

            game.played_time = played_time
            game.time_to_beat = time_to_beat

            game.title = request.POST.get('title', game.title)
            game.genre = request.POST.get('genre', game.genre)
            game.platform = request.POST.get('platform', game.platform)
            game.developer = request.POST.get('developer', game.developer)
            game.publisher = request.POST.get('publisher', game.publisher)
            game.status = request.POST.get('status', game.status)
            game.ranking = int(request.POST.get('ranking', game.ranking))
            game.rating = request.POST.get('rating', game.rating)

            game.save()
            return redirect('/game/')
    except Exception as e:
        print("view.update_game: error = ", e)
        return redirect('/game/')

def get_games(request, status, platform, page):
    if platform == 'All':
        game_list = Game.objects.filter(status=status).order_by('title')
    else:
        game_list = Game.objects.filter(status=status, platform=platform).order_by('title')
    paginator = Paginator(game_list, 30)
    page_obj = paginator.get_page(page)
    
    # games = serializers.serialize('json', page_obj)

    games = []
    for game in page_obj:
        games.append({
            'id': str(game._id),
            'title': game.title,
            'genre': game.genre,
            'platform': game.platform,
            'developer': game.developer,
            'publisher': game.publisher,
            'status': game.status,
            'played_time': game.played_time,
            'time_to_beat': game.time_to_beat,
            'ranking': game.ranking,
            'rating': game.rating,
        })

    data = {
        'games': games,
        'page': page_obj.number,
        'pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
    }
    # return JsonResponse(data, safe=False)
    return JsonResponse(data, encoder=CustomJSONEncoder, safe=False)

def badge(request, status):
    played_count = Game.objects.filter(status='Played').count()
    playing_count = Game.objects.filter(status='Playing').count()
    to_play_count = Game.objects.filter(status='ToPlay').count()

    all_platform = Game.objects.filter(status=status).count()
    pc = Game.objects.filter(status=status, platform='PC').count()
    playstation = Game.objects.filter(status=status, platform='PlayStation').count()
    nintendo_switch = Game.objects.filter(status=status, platform='Nintendo Switch').count()
    xbox = Game.objects.filter(status=status, platform='Xbox').count()
    mobile = Game.objects.filter(status=status, platform='Mobile').count()
    
    return JsonResponse({
        'played': played_count,
        'playing': playing_count,
        'to_play': to_play_count,
        'all_platform': all_platform,
        'pc': pc,
        'playstation': playstation,
        'nintendo_switch': nintendo_switch,
        'xbox': xbox,
        'mobile': mobile
    })

@api_view(['DELETE'])
def delete_game(request, id):
    game = get_object_or_404(Game, _id=ObjectId(id))
    game.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)