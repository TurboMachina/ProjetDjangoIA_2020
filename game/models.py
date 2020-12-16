from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from ai.models import Esperance, AI


class Game(models.Model) : 
    currentUser = models.IntegerField(null=True, blank=True)
    gameState = ArrayField(ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True), null=True, blank=True)
    # grâce à related_name la classe User aura un attribut games
    # through permet de donner un Model comme table intermédiaire
    players = models.ManyToManyField(User, related_name="games", through="UserGame")
    ias = models.ManyToManyField(AI, related_name="games", through="UserGame")
    winner = models.IntegerField(null=True, blank=True)


class UserGame(models.Model) : 
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    ia = models.ForeignKey(AI, on_delete=models.CASCADE, null=True, blank=True)
    color = models.IntegerField()
    userNumber = models.IntegerField()
    posUserX = models.IntegerField(null=True, blank=True)
    posUserY = models.IntegerField(null=True, blank=True)
    movePrecedent = models.ForeignKey(Esperance, on_delete=models.DO_NOTHING, related_name="userGames",null=True, blank=True)
