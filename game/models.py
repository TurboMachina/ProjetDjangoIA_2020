from django.db import models
from django.contrib.postgres.fields import ArrayField

class Game(models.Model) : 
    id = models.IntegerField()
    currentUser = models.IntegerField()
    gameState = modesl.ArrayField()
