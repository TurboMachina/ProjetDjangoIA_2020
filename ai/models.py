from django.db import models
from django.contrib.postgres.fields import ArrayField
from ai.validators import *
from django.core.validators import MaxValueValidator, MinValueValidator


class State(models.Model):
    posXUser1 = models.IntegerField()
    posYUser1 = models.IntegerField()
    posXUser2 = models.IntegerField()
    posYUser2 = models.IntegerField()
    turn = models.IntegerField()
    game_sate = ArrayField(ArrayField(models.IntegerField()))


class AI(models.Model):
    epsilon_greedy = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    learning_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    gamma = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    states = models.ManyToManyField(State)


class Move(models.Model):
    moveY = models.IntegerField(null=True, blank=True)
    moveX = models.IntegerField(null=True, blank=True)


class Esperance(models.Model):
    state = models.ForeignKey(State, on_delete = models.CASCADE)
    move = models.ForeignKey(Move, on_delete=models.CASCADE)
    esperance = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
