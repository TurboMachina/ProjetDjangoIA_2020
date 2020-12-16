from django.db import models
from django.contrib.postgres.fields import ArrayField
from ai.validators import *


class State(models.Model):
    posXUser1 = models.IntegerField()
    posYUser1 = models.IntegerField()
    posXUser2 = models.IntegerField()
    posYUser2 = models.IntegerField()
    turn = MinMaxFloat(min_value=1, max_value=2)
    game_sate = ArrayField(ArrayField(models.IntegerField()))


class AI(models.Model):
    epsilon_greedy = MinMaxFloat(min_value=0, max_value=1)
    learning_rate = MinMaxFloat(min_value=0, max_value=1)
    gamma = MinMaxFloat(min_value=0, max_value=1)
    states = models.ManyToManyField(State)


class Move(models.Model):
    moveY = models.IntegerField(null=True, blank=True)
    moveX = models.IntegerField(null=True, blank=True)


class Esperance(models.Model):
    state = models.ForeignKey(State, on_delete = models.CASCADE)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    esperance = MinMaxFloat(min_value=0, max_value=1)
