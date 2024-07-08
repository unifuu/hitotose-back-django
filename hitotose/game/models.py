from dataclasses import dataclass, field
from djongo import models
from bson import ObjectId

class Game(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    title  = models.CharField(max_length=100)
    genre = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    developer = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    played_time = models.IntegerField()
    time_to_beat = models.IntegerField()
    ranking = models.IntegerField()
    rating = models.CharField(max_length=3)

    class Meta:
        db_table = "game"

@dataclass
class Bagde:
    played: int
    playing: int
    to_played: int