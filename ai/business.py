import numpy as np
from random import randint
import random
from game.DTO import Game
from game.DTO import User
from ai.models import *
from game.models import *
from django.db.models import Max


def take_action(epsilon, state, possible_moves):
    possible_esperances = []
    if random.uniform(0, 1) < epsilon:
        action = possible_moves[randint(0, len(possible_moves))]
    else:
        for move in possible_moves : 
            moveId.id = Move.objects.get(moveY=move[0], moveX=move[1])
            possible_esperances.append(Esperance.objects.get(esperance__id=moveId.id))

        best_esperance = max(possible_esperances.esperance)
        action = Move.objects.get(id = best_esperance.move)

    return action


def reward(game_state) : 
    nb_cells_player1 = 0
    nb_cells_player2 = 0
    for line in game_state:
        nb_cells_player1 += line.count(1)
        nb_cells_player2 += line.count(2)
    return nb_cells_player1 - nb_cells_player2


def play(epsilon, learning_rate, gama, stateId, posXUser1, posYUser1, posXUser2, posYUser2, game_state, userGame, possible_moves):
    try : 
        state = State.objects.get(id = stateId, posXUser1 = posXUser1, posYUser1 = posYUser1, posXUser2 = posXUser2, posYUser2 = posYUser2, game_sate = game_sate)
    except SomeModel.DoesNotExist :
        state = None

    if state == None :
        state = State.objects.create(id = stateId, posXUser1 = posXUser1, posYUser1 = posYUser1, posXUser2 = posXUser2, posYUser2 = posYUser2, game_sate = game_sate)

    action = take_action(epsilon, state, possible_moves)

    prevEsp = Esperance.objects.filter(userGames__id=userGame.id).first()

    action_reward = reward(game_state)
    
    nextAction = take_action(0.0, state, possible_moves) 

    current_esperance.esperance = Esperance.objects.get(fk = state, fk = action)

    current_esperance.esperance = current_esperance.esperance + learning_rate * (action_reward + gama * prevEsp.esperance - current_esperance.esperance))
    current_esperance.esperance.save()

    return action

