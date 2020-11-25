from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

class Game(models.Model) : 
    currentUser = models.IntegerField(null=True, blank=True)
    gameState = ArrayField(ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True), null=True, blank=True)
    # grâce à related_name la classe User aura un attribut games
    # through permet de donner un Model comme table intermédiaire
    players = models.ManyToManyField(User, related_name="games", through="UserGame")
    winner = models.IntegerField(null=True, blank=True)

class UserGame(models.Model) : 
    userId = models.ForeignKey(User, on_delete = models.CASCADE)
    game = models.ForeignKey(Game, on_delete = models.CASCADE)
    color = models.IntegerField()
    userNumber = models.IntegerField()
    posUserX = models.IntegerField(null=True, blank=True)
    posUserY = models.IntegerField(null=True, blank=True)

