from django.db import models
from django.contrib.postgres.fields import ArrayField
from connection.models import User

class Game(models.Model) : 
    id = models.IntegerField(primary_key=True)
    currentUser = models.IntegerField()
    gameState = ArrayField(ArrayField(models.IntegerField()))

class UserGame(models.Model) : 
    userId = models.ForeignKey(User,on_delete = models.CASCADE)
    game = models.ForeignKey(Game,on_delete = models.CASCADE)
    color = models.IntegerField()
    userNumber = models.IntegerField()
    posUserX = models.IntegerField()
    posUserY = models.IntegerField()

