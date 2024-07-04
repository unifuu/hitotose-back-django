from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from bson import ObjectId
from .models import Game
from .serializers import GameSerializer

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

def get_game_by_id(request, id):
    print("game_by_id.id=", id)
    game = get_object_or_404(Game, _id=ObjectId(id))
    print("game_by_id.game=", game)
    serializer = GameSerializer(game)
    return JsonResponse(serializer.data)

@api_view(['POST'])
def create_game(request):
    if request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
def update_game(request, id):
    if not ObjectId.is_valid(id):
        return Response({'error': 'Invalid ID format'}, status=status.HTTP_400_BAD_REQUEST)
    
    game = get_object_or_404(Game, _id=ObjectId(id))
    if request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)