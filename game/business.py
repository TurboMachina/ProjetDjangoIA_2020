from django.db.models import Count

from game.DTO import *
import random
import game.models as models
from game.error import *
from game.mapper import *


# Joueur random pour debuter game
def random_user_number() : 
    return random.randint(1,2)

#_______________________________________________________________________________
# FONCTION PRINCIPALE POUR JOUER
#_______________________________________________________________________________

def assign_pos(userGame, posX, posY=None) :
    if not posY :
        posY = posX
    userGame.posUserX = posX
    userGame.posUserY = posY

def start_game(game_id, user) :
    games = models.Game.objects.annotate(Count("players"))
    game = games.filter(id=game_id, players__id=user.id, gameState__isnull=True, players__count=2).first()
    if not game :
        raise StartGameError()
    
    gameDTO = Game(game_id)
    gameDTO.init_board()

    game.gameState = gameDTO.gameState
    game.currentUser = random_user_number()
    game.save()

    userGames = models.UserGame.objects.filter(game__id=game.id)

    for userGame in userGames :
        if userGame.userNumber == 1 :
            assign_pos(userGame, 0)
        elif userGame.userNumber == 2 :
            assign_pos(userGame, gameDTO.col_size - 1)
        userGame.save()

    return game


def apply_move(game_id, user, movement) :
    userGame = models.UserGame.objects.filter(game__id=game_id, userId__id=user.id).first()
    if not userGame :
        raise NotPlayerError()
    
    if not userGame.game.gameState :
        raise GameNotStartedError()
    
    if not userGame.userNumber == userGame.game.currentUser :
        raise NotYourTurnError()
    

    game = userGame.game
    gameDTO = mapGame(game)
    if not gameDTO.winner :
        newPosX = userGame.posUserX + movement["x"]
        newPosY = userGame.posUserY + movement["y"]
        if not gameDTO.movement_ok({"x" : newPosX, "y" : newPosY}, gameDTO.turn) :
            raise InvalidMoveError()
        
        gameDTO.update_board(gameDTO.turn, {"posX" : newPosX, "posY" : newPosY})
        if gameDTO.game_over() :
            gameDTO.winner = gameDTO.get_winner()
        gameDTO.next_turn()

        userGame.posUserX = newPosX
        userGame.posUserY = newPosY
        userGame.save()
    
        game.gameState = gameDTO.gameState
        game.currentUser = gameDTO.turn
        game.winner = gameDTO.winner
        game.save()

    userGames = models.UserGame.objects.filter(game__id=game.id)
    gameDTO.players = mapMultipleUsers(userGames)

    return gameDTO


def resume_game(game_id, user_id) :
    game = models.Game.objects.filter(id=game_id, players__id=user_id).first()
    if not game :
        raise NotPlayerError()

    gameDTO = mapGame(game)
    userGames = models.UserGame.objects.filter(game__id=game_id).all()
    gameDTO.players = mapMultipleUsers(userGames)
    return gameDTO


def launch_game():
    player1 = models.User(1, "aherrent", "abcd")
    player2 = models.User(2, "abaert", "password")


def my_games(user) :
    return models.Game.objects.filter(players=user).all()


def create_game(form, user_id) :
    if not form.is_valid() :
        raise ColorInvalidError()
        
    game = models.Game.objects.create()
    user = models.User.objects.get(pk=user_id)

    hex_color = int(form.cleaned_data["hex_color"].replace("#", ""), 16)

    if hex_color == 0 :
        raise ForbidenColorError()

    models.UserGame.objects.create(userId=user, game=game, color=hex_color, userNumber=1)
    
    return game


def joinable_games(user) :
    games = models.Game.objects.annotate(Count("players"))
    games = games.filter(players__count__lte=2, gameState__isnull=True).exclude(players=user)
    return games


def join_game(game_id, user, form) :
    game = models.Game.objects.get(id=game_id)
    players = game.players.all()
    if user in players :
        raise AlreadyPlayerError()

    if len(players) == 2 :
        raise AlreadyTwoPlayerError()
    
    if not form.is_valid() :
        raise ColorInvalidError()
    hex_color = int(form.cleaned_data["hex_color"].replace("#", ""), 16)

    if hex_color == 0 :
        raise ForbidenColorError()
    if models.UserGame.objects.filter(game__id=game_id, color=hex_color).exists() :
        raise ColorAlreadyTakenError()
    
    models.UserGame.objects.create(userId=user, game=game, color=hex_color, userNumber=2)

"""
# Entrainement des IA, (IA contre IA)
def train(self, ia1, ia2, number_games) :
    players = [ia1, ia2]
    game = Game(players) # ajout params 

    for game in range(number_games) : 
        play(game)
    

"""