from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

def game_by_id(request, id):
    print("game_by_id.id=", id)
    game = get_object_or_404(Game, _id=id)
    print("game_by_id.game=", game)
    serializer = GameSerializer(game)
    return JsonResponse(serializer.data)