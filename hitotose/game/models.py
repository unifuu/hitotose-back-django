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

    # played_time_hour = models.IntegerField(blank=True, null=True)
    # played_time_min = models.IntegerField(blank=True, null=True)
    # time_to_beat_hour = models.IntegerField(blank=True, null=True)
    # time_to_beat_min = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "game"

    # def save(self, *args, **kwargs):
    #     if self.played_time_hour is not None and self.played_time_min is not None:
    #         if self.played_time_hour != "" and self.played_time_min != "":
    #             self.played_time = self.played_time_hour * 60 + self.played_time_min

    #     if self.time_to_beat_hour is not None and self.time_to_beat_min is not None:
    #         if self.time_to_beat_hour != "" and self.time_to_beat_min != "":
    #             self.time_to_beat = self.time_to_beat_hour * 60 + self.time_to_beat_min
    #     super().save(*args, **kwargs)

@dataclass
class Bagde:
    played: int
    playing: int
    to_played: int