#-----------------------------------------------------------------------------------------------
# AI's logic
#-----------------------------------------------------------------------------------------------

from random import randint
import random
from ai.error import NotValidAIError
from game.DTO import Game
from game.DTO import User
from ai.models import *
from django.db.models import Max, Q
from django.core.exceptions import ObjectDoesNotExist


def take_action(epsilon, state, possible_moves):
    esp = 0
    if random.uniform(0, 1) < epsilon:
        # print("explore")
        action = possible_moves[randint(0, len(possible_moves)) - 1]
        esp = Esperance.objects.filter(state__id=state.id, move__moveX=action[0], move__moveY=action[1]).first()
    else:
        # print("exploite")
        best_esperance = Esperance.objects.filter(state__id=state.id).order_by("-esperance").first()
        esps = Esperance.objects.filter(state_id=state.id)
        # for esp in esps :
            # print(esp.esperance)
        # print("best")
        # print(best_esperance.esperance)
        action = [best_esperance.move.moveX, best_esperance.move.moveY]
        esp = best_esperance

    return action, esp


def reward(game_state, player_number) : 
    nb_cells_player = 0
    nb_cells_oponent = 0
    oponent_number = (player_number % 2) + 1
    for line in game_state:
        nb_cells_player += line.count(player_number)
        nb_cells_oponent += line.count(oponent_number)
    return nb_cells_player - nb_cells_oponent


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

    # for line in game_state :
    #     lineStr = "["
    #     for elem in line :
    #         lineStr += str(elem)
    #     print(lineStr + "]")

    if prevEsp :
        action_reward = reward(game_state, turn)
        
        __, best_current_esperance = take_action(0.0, state, possible_moves) 

        prevEsp.esperance = prevEsp.esperance + userGame.ia.learning_rate * (float(action_reward) + userGame.ia.gamma * best_current_esperance.esperance - prevEsp.esperance)
        prevEsp.save()
    userGame.movePrecedent = current_esp
    userGame.save()

    return action[0], action[1]


def create_ia(form) :
    if not form.is_valid() :
        raise NotValidAIError()
    epsilon = form.cleaned_data["epsilonGreedy"]
    learningRate = form.cleaned_data["learningRate"]
    gamma = form.cleaned_data["gamma"]

    ia = AI.objects.create(epsilon_greedy=epsilon, learning_rate=learningRate, gamma=gamma)

    return ia 


def list_ia() :
    ia_list = AI.objects.all()
    return ia_list