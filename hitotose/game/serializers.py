from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    
    class Meta:
        model = Game
        fields = '__all__'