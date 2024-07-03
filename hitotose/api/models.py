from djongo import models
from bson import ObjectId

# Create your models here.
class Game(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId, editable=False)
    title  = models.CharField(max_length=100)
    genre = models.CharField(max_length=20)
    platform = models.CharField(max_length=20)
    developer_id = models.CharField(max_length=40)
    publisher_id = models.CharField(max_length=40)
    status = models.CharField(max_length=10)
    total_time = models.IntegerField()
    how_long_to_beat = models.IntegerField()
    ranking = models.IntegerField()
    rating = models.CharField(max_length=3)

    class Meta:
        db_table = "game"