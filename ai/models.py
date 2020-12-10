from django.db import models
from django.contrib.postgres.fields import ArrayField


class AI(models.Model) : 
    epsilon_greedy = models.FloatField(min=0, max=1)
    learning_rate = models.FloatField(min=0, max=1)
    gama = models.FloatField(min=0, max=1)
    states = models.ManyToManyField(State) 

class State(models.Model) : 
    posXUser1 = models.IntegerField()
    posYUser1 = models.IntegerField()
    posXUser2 = models.IntegerField()
    posYUser2 = models.IntegerField()
    turn = models.IntegerField(min=1, max=2)
    game_sate = ArrayField(ArrayField(models.IntegerField()))


class Esperance(models.Model) : 
    state = models.ForeignKey(State, on_delete = models.CASCADE)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    esperance = models.FloatField(min=0, max=1)




class Move(models.Model) : 
    moveY = models.IntegerField(null=True, blank=True)
    moveX = models.IntegerField(null=True, blank=True)

