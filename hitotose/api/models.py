from django.db import models

# Create your models here.
class Game(models.Model):
    id = models.CharField(max_length=40)
    title  = models.CharField(max_length=100)
    genres = models.JSONField()
    platform = models.CharField(max_length=20)
    developer_id = models.CharField(max_length=40)
    publisher_id = models.CharField(max_length=40)
    status = models.CharField(max_length=10)
    played_time = models.IntegerField()
    how_long_to_beat = models.IntegerField()
    ranking = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.title