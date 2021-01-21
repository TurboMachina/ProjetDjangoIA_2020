# -----------------------------------------------------------------------------------------------
# AI's logic
# -----------------------------------------------------------------------------------------------

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
        print("explore")
        action = possible_moves[randint(0, len(possible_moves)) - 1]
        esp = Esperance.objects.filter(state__id=state.id, move__moveX=action[0], move__moveY=action[1]).first()
    else:
        print("exploite")
        best_esperance = Esperance.objects.filter(state__id=state.id).order_by("-esperance").first()
        esps = Esperance.objects.filter(state_id=state.id)
        for esp in esps:
            print(esp.esperance)
        print("best")
        print(best_esperance.esperance)
        action = [best_esperance.move.moveX, best_esperance.move.moveY]
        esp = best_esperance

    return action, esp


def reward(game_state, player_number):
    nb_cells_player = 0
    nb_cells_opponent = 0
    opponent_number = (player_number % 2) + 1
    for line in game_state:
        nb_cells_player += line.count(player_number)
        nb_cells_opponent += line.count(opponent_number)
    return nb_cells_player - nb_cells_opponent


def play(pos_x_user1, pos_y_user1, pos_x_user2, pos_y_user2, game_state, user_game, possible_moves, turn):
    try:
        state = State.objects.get(turn=turn, posXUser1=pos_x_user1, posYUser1=pos_y_user1, posXUser2=pos_x_user2,
                                  posYUser2=pos_y_user2, game_sate=game_state)
    except ObjectDoesNotExist:
        state = State.objects.create(turn=turn, posXUser1=pos_x_user1, posYUser1=pos_y_user1, posXUser2=pos_x_user2,
                                     posYUser2=pos_y_user2, game_sate=game_state)
        query = Q()
        for move in possible_moves:
            query = query | Q(moveX=move[0], moveY=move[1])
        moves = Move.objects.filter(query)
        for move in moves:
            Esperance.objects.create(move=move, state=state, esperance=0)

    action, current_esp = take_action(user_game.ia.epsilon_greedy, state, possible_moves)
    prev_esp = Esperance.objects.filter(userGames__id=user_game.id).first()

    for line in game_state:
        line_str = "["
        for elem in line:
            line_str += str(elem)
        print(line_str + "]")

    if prev_esp:
        action_reward = reward(game_state, turn)

        __, best_current_esperance = take_action(0.0, state, possible_moves)

        prev_esp.esperance = prev_esp.esperance + user_game.ia.learning_rate * (
                    float(action_reward) + user_game.ia.gamma * best_current_esperance.esperance - prev_esp.esperance)
        prev_esp.save()
    user_game.movePrecedent = current_esp
    user_game.save()

    return action[0], action[1]


def create_ia(form):
    if not form.is_valid():
        raise NotValidAIError()
    epsilon = form.cleaned_data["epsilonGreedy"]
    learning_rate = form.cleaned_data["learningRate"]
    gamma = form.cleaned_data["gamma"]

    ia = AI.objects.create(epsilon_greedy=epsilon, learning_rate=learning_rate, gamma=gamma)

    return ia


def list_ia():
    ia_list = AI.objects.all()
    return ia_list
