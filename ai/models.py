from django.db import models

class AI(models.Model) : 
    id_ai = models.IntegerField(null=False, blank=True)
    epsilon_greedy = models.FloatField(null=True, blank=True)
    learning_rate = models.FloatField(null=True, blank=True)
    gama = models.FloatField(null=True, blank=True)
    states = models.ManyToManyField(State)

class State(models.Model) : 
    id_state = models.IntegerField(null=False, blank=True)
    posXUser1 = models.IntegerField(null=True, blank=True)
    posYUser1 = models.IntegerField(null=True, blank=True)
    posXUser2 = models.IntegerField(null=True, blank=True)
    posYUser2 = models.IntegerField(null=True, blank=True)
    game_sate = ArrayField(ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True), null=True, blank=True)


class Esperance(models.Model) : 
    state = models.ForeignKey(State, on_delete = models.CASCADE)
    move = models.ForeignKey(Move, on_delete = models.CASCADE)
    esperance = 


class Move(models.Model) : 
    id_move = models.IntegerField(null=False, blank=True)
    moveY = models.IntegerField(null=True, blank=True)
    moveX = models.IntegerField(null=True, blank=True)

