from rest_framework import serializers
from .models import Game

class GameSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='_id', read_only=True)
    played_time = serializers.IntegerField(required=False)
    time_to_beat = serializers.IntegerField(required=False)
    ranking = serializers.IntegerField(required=False)
    rating = serializers.CharField(required=False)

    # played_time_hour = serializers.IntegerField(required=False)
    # played_time_min = serializers.IntegerField(required=False)
    # time_to_beat_hour = serializers.IntegerField(required=False)
    # time_to_beat_min = serializers.IntegerField(required=False)
    
    class Meta:
        model = Game
        fields = '__all__'