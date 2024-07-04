from django.apps import AppConfig
from .stopwatch import Stopwatch

class GameConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'game'

    def ready(self):
        self.stopwatch = Stopwatch()