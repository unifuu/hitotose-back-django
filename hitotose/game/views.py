from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
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

class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

def get_game_by_id(request, id):
    game = get_object_or_404(Game, _id=ObjectId(id))
    serializer = GameSerializer(game)
    return JsonResponse(serializer.data)

def get_title_by_id(id):
    game = get_object_or_404(Game, _id=ObjectId(id))
    serializer = GameSerializer(game)
    return serializer.data['title']

def start_game(request, id):
    app_config = apps.get_app_config('game')
    stopwatch = app_config.stopwatch

    print('start_game.stopwatch:', stopwatch)

    if stopwatch.game_id is None or stopwatch.game_id == '':
        stopwatch.game_id = id
        stopwatch.game_title = get_title_by_id(id)
        stopwatch.start_time = datetime.now()
        stopwatch.end_time = ''
        stopwatch.duration = 0
        print('stopwatch: ', stopwatch)
        return JsonResponse({'message': stopwatch.to_dict()})
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

def stop_game(request, id):
    app_config = apps.get_app_config('game')
    stopwatch = app_config.stopwatch

    if stopwatch is not None:
        if stopwatch.game_id == id:
            
            # Get duration
            stopwatch.end_time = datetime.now()
            duration = stopwatch.end_time - stopwatch.start_time
            total_seconds = duration.total_seconds()
            stopwatch.duration = total_seconds // 60

            game = get_object_or_404(Game, _id=ObjectId(id))
            game.played_time += stopwatch.duration
            game.save()

            # Game.objects.filter(_id=ObjectId(id)).update(duration=game.duration + stopwatch.duration)

            stopwatch.clear()
            return JsonResponse({'message': 'Ended!'})
        else:
            return JsonResponse({'message': 'The game is not running...'})
    else:
        return JsonResponse({'message': 'No active game!'})

@api_view(['POST'])
def create_game(request):
    if request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_protect
def update_game(request, id):
    if not ObjectId.is_valid(id):
        return Response({'error': 'Invalid ID format'}, status=status.HTTP_400_BAD_REQUEST)
    
    game = get_object_or_404(Game, _id=ObjectId(id))
    if request.method == 'GET':
            game = get_object_or_404(Game, _id=ObjectId(id))
            serializer = GameSerializer(game)
            return JsonResponse(serializer.data)
    else:
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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