from django.db import models
from levelupapi.models.gamer import Gamer
from levelupapi.models.game import Game

class Event(models.Model):

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    description = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(Gamer, on_delete=models.CASCADE)