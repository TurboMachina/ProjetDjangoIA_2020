# -----------------------------------------------------------------------------------------------
# Logic of a game
# -----------------------------------------------------------------------------------------------

from django.db.models import Count, Q
from game.DTO import *
import random
import game.models as gmodels
from game.error import *
from game.mapper import *
from ai.business import play
from ai.models import *


def random_user_number():
    return random.randint(1, 2)


def ia_plays(user_game, iaDTO, game, game_dto):
    user_game.move()
    if game.game_over():
        game_dto.winner = game_dto.get_winner()
    game_dto.next_turn()


def maj_pos(new_pos_x, new_pos_y, game_dto):
    if not game_dto.movement_ok({"x": new_pos_x, "y": new_pos_y}, game_dto.turn):
        raise InvalidMoveError()
    game_dto.update_board(game_dto.turn, {"posX": new_pos_x, "posY": new_pos_y})
    if game_dto.game_over():
        game_dto.winner = game_dto.get_winner()
    game_dto.next_turn()


def move(user_game, move_x, move_y, game_dto):
    new_pos_x = user_game.posUserX + move_x
    new_pos_y = user_game.posUserY + move_y
    maj_pos(new_pos_x, new_pos_y, game_dto)
    return new_pos_x, new_pos_y


def save_user_game(user_game, new_pos_x, new_pos_y):
    user_game.posUserX = new_pos_x
    user_game.posUserY = new_pos_y
    user_game.save()


def save_game_state(game, game_dto):
    game.gameState = game_dto.gameState
    game.currentUser = game_dto.turn
    game.winner = game_dto.winner
    game.save()


def save_move(user_game, new_pos_x, new_pos_y, game, game_dto):
    save_user_game(user_game, new_pos_x, new_pos_y)
    save_game_state(game, game_dto)


def assign_pos(user_game, pos_x, pos_y=None):
    if not pos_y:
        pos_y = pos_x
    user_game.posUserX = pos_x
    user_game.posUserY = pos_y
    user_game.save()


def assign_duo(user_game1, user_game2):
    assign_pos(user_game1, 0)
    assign_pos(user_game2, 7)


def start_game(game_id, user):
    games = gmodels.Game.objects.annotate(Count("players"))
    games = games.annotate(Count("ias"))
    query = (Q(players__count=2) | Q(players__count=1, ias__count=1))
    games = games.filter(query)
    game = games.filter(id=game_id, players__id=user.id, gameState__isnull=True).first()
    if not game:
        raise StartGameError()

    gameDTO = Game(game_id)
    gameDTO.init_board()
    gameDTO.turn = random_user_number()

    save_game_state(game, gameDTO)

    user_games = gmodels.UserGame.objects.filter(game__id=game.id)

    if user_games[0].userNumber == 1:
        assign_duo(user_games[0], user_games[1])
        user_game1, user_game2 = user_games[0], user_games[1]
    else:
        assign_duo(user_games[1], user_games[0])
        user_game1, user_game2 = user_games[1], user_games[0]

    if user_game2.ia and user_game2.userNumber == gameDTO.turn:
        (moveX, moveY) = play(user_game1.posUserX, user_game1.posUserY, user_game2.posUserX, user_game2.posUserY,
                              gameDTO.gameState, user_game2,
                              gameDTO.possible_actions(user_game2.posUserX, user_game2.posUserY, user_game2.userNumber),
                              gameDTO.turn)
        (newPosX, newPosY) = move(user_games[1], moveX, moveY, gameDTO)
        save_move(user_games[1], newPosX, newPosY, game, gameDTO)

    return game


def apply_move(game_id, user, movement):
    user_game = gmodels.user_game.objects.filter(game__id=game_id, userId__id=user.id).first()
    if not user_game:
        raise NotPlayerError()

    if not user_game.game.gameState:
        raise GameNotStartedError()

    if not user_game.userNumber == user_game.game.currentUser:
        raise NotYourTurnError()

    game = user_game.game
    user_game2 = gmodels.user_game.objects.filter(game__id=game.id).exclude(userId__id=user.id).first()
    gameDTO = mapGame(game)
    if not gameDTO.winner:
        (newPosX, newPosY) = move(user_game, movement["x"], movement["y"], gameDTO)
        print("test")

        if user_game2.ia and not gameDTO.game_over():
            (moveX, moveY) = play(newPosX, newPosY, user_game2.posUserX, user_game2.posUserY, gameDTO.gameState,
                                  user_game2, gameDTO.possible_actions(user_game2.posUserX, user_game2.posUserY,
                                                                      user_game2.userNumber), gameDTO.turn)
            (newPosXAi, newPosYAi) = move(user_game2, moveX, moveY, gameDTO)
            save_user_game(user_game2, newPosXAi, newPosYAi)

        save_move(user_game, newPosX, newPosY, game, gameDTO)

    gameDTO.players = mapMultipleUsers([user_game, user_game2])

    return gameDTO


def resume_game(game_id, user_id):
    game = gmodels.Game.objects.filter(id=game_id, players__id=user_id).first()
    if not game:
        raise NotPlayerError()

    gameDTO = mapGame(game)
    user_games = gmodels.user_game.objects.filter(game__id=game_id).all()
    gameDTO.players = mapMultipleUsers(user_games)
    return gameDTO


def my_games(user):
    return gmodels.Game.objects.filter(players=user).all()


def create_game(form, user_id):
    if not form.is_valid():
        raise ColorInvalidError()

    game = gmodels.Game.objects.create()
    user = gmodels.User.objects.get(pk=user_id)

    hex_color = int(form.cleaned_data["hex_color"].replace("#", ""), 16)

    if hex_color == 0:
        raise ForbidenColorError()

    gmodels.user_game.objects.create(userId=user, game=game, color=hex_color, userNumber=1)

    return game


def joinable_games(user):
    games = gmodels.Game.objects.annotate(Count("players"))
    games = games.filter(players__count__lte=2, gameState__isnull=True).exclude(players=user)
    return games


def verrification_before_join(label, form, game_id):
    game = gmodels.Game.objects.get(id=game_id)

    players = game.players.all()
    ias = game.ias.all()

    if len(players) == 2 or len(players) == 1 and len(ias) == 1:
        raise AlreadyTwoPlayerError()

    if not form.is_valid():
        raise ColorInvalidError()
    hex_color = int(form.cleaned_data[label].replace("#", ""), 16)

    if hex_color == 0:
        raise ForbidenColorError()
    if gmodels.user_game.objects.filter(game__id=game_id, color=hex_color).exists():
        raise ColorAlreadyTakenError()

    return game, hex_color


def join_ia(game_id, ia_id, form):
    game, hex_color = verrification_before_join("ia_color", form, game_id)

    ai = AI.objects.filter(id=ia_id).first()

    gmodels.user_game.objects.create(ia=ai, game=game, color=hex_color, userNumber=2)


def join_game(game_id, user, form):
    game, hex_color = verrification_before_join("hex_color", form, game_id)

    if user in game.players.all():
        raise AlreadyPlayerError()

    gmodels.user_game.objects.create(userId=user, game=game, color=hex_color, userNumber=2)


def train(ia_id, form):
    if not form.is_valid():
        raise NumberOfGameNotValid()
    nb_games = int(form.cleaned_data["numberOfGames"])
    for __ in range(nb_games):
        game = gmodels.Game.objects.create()

        ia = AI.objects.filter(id=ia_id).first()

        user_game1 = gmodels.user_game.objects.create(game=game, ia=ia, color=0, userNumber=1)
        user_game2 = gmodels.user_game.objects.create(game=game, ia=ia, color=1, userNumber=2)
        user_games = [user_game1, user_game2]

        gameDTO = mapGame(game)
        gameDTO.init_board()
        gameDTO.turn = random_user_number()

        save_game_state(game, gameDTO)

        assign_duo(user_game1, user_game2)

        while not gameDTO.game_over():
            current_user_game = user_games[gameDTO.turn - 1]
            (moveX, moveY) = play(user_game1.posUserX, user_game1.posUserY, user_game2.posUserX, user_game2.posUserY,
                                  gameDTO.gameState, current_user_game,
                                  gameDTO.possible_actions(current_user_game.posUserX, current_user_game.posUserY,
                                                           current_user_game.userNumber), gameDTO.turn)
            (newPosX, newPosY) = move(current_user_game, moveX, moveY, gameDTO)
            save_move(current_user_game, newPosX, newPosY, game, gameDTO)
