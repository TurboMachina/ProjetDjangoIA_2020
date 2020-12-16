from random import randint
import random
from game.DTO import Game
from game.DTO import User
from ai.models import *
from django.db.models import Max, Q
from django.core.exceptions import ObjectDoesNotExist


def take_action(epsilon, state, possible_moves):
    esp = 0
    if random.uniform(0, 1) < epsilon:
        action = possible_moves[randint(0, len(possible_moves))]
        esp = Esperance.objects.filter(state__id=state.id, move__moveX=action[0], move__moveY=action[1])
    else:
        best_esperance = Esperance.objects.filter(state__id=state.id).order_by("-esperance").first()

        action = [best_esperance.move.moveX, best_esperance.move.moveY]
        esp = best_esperance

    return action, esp


def reward(game_state) : 
    nb_cells_player1 = 0
    nb_cells_player2 = 0
    for line in game_state:
        nb_cells_player1 += line.count(1)
        nb_cells_player2 += line.count(2)
    return nb_cells_player1 - nb_cells_player2


def play(posXUser1, posYUser1, posXUser2, posYUser2, game_state, userGame, possible_moves, turn):
    try : 
        state = State.objects.get(turn=turn, posXUser1=posXUser1, posYUser1=posYUser1, posXUser2=posXUser2, posYUser2=posYUser2, game_sate=game_state)
    except ObjectDoesNotExist:
        state = State.objects.create(turn=turn, posXUser1=posXUser1, posYUser1=posYUser1, posXUser2=posXUser2, posYUser2=posYUser2, game_sate=game_state)
        query = Q()
        for move in possible_moves:
            query = query | Q(moveX=move[0], moveY=move[1])
        moves = Move.objects.filter(query)
        for move in moves:
            Esperance.objects.create(move=move, state=state, esperance=0)

    action, current_esp = take_action(userGame.ia.epsilon_greedy, state, possible_moves)

    prevEsp = Esperance.objects.filter(userGames__id=userGame.id).first()

    if prevEsp :
        action_reward = reward(game_state)
        
        __, best_current_esperance = take_action(0.0, state, possible_moves) 

        #current_esperance.esperance = Esperance.objects.get(fk = state, fk = action)

        #prevEsp.esperance = current_esperance.esperance + learning_rate * (action_reward + gama * prevEsp.esperance - current_esperance.esperance))
        prevEsp.esperance = prevEsp.esperance + userGame.ia.learning_rate * (action_reward + userGame.ia.gamma * best_current_esperance - prevEsp.esperance)
        prevEsp.save()
    
    userGame.movePrecedent = current_esp
    userGame.save()

    return action[0], action[1]


def create_ia(form) :
    if not form.is_valid() :
        pass
    epsilon = form.cleaned_data["epsilonGreedy"]
    learningRate = form.cleaned_data["learningRate"]
    gamma = form.cleaned_data["gamma"]

    ia = AI.objects.create(epsilon_greedy=epsilon, learning_rate=learningRate, gamma=gamma)

    return ia 


def list_ia() :
    ia_list = AI.objects.all()
    return ia_list