from django.db.models import Count

from game.DTO import *
import random
import game.models as models
from game.error import *
from game.mapper import *
from game.IA import IA


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
        if userGame.ia and userGame.userNumber == game.currentUser :
            ia_plays(userGame, mapIA(userGame), game, gameDTO)
        userGame.save()

    return game

def ia_plays(userGame, iaDTO, game, gameDTO) :
    userGame.move()
    if game.game_over() :
        gameDTO.winner = gameDTO.get_winner()
    gameDTO.next_turn() # TODO recup le move et mettre à jour le userGame


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
        
        userGame2 = models.UserGame.objects.filter(game__id=game.id).exclude(userId__id=user.id).first()
        if userGame2.ia and not gameDTO.game_over():
            ia_plays(userGame2, mapIA(userGame2), game, gameDTO) #TODO à changer pour s'adapté à l'ia

        userGame.posUserX = newPosX
        userGame.posUserY = newPosY
        userGame.save()
    
        game.gameState = gameDTO.gameState
        game.currentUser = gameDTO.turn
        game.winner = gameDTO.winner
        game.save()

    gameDTO.players = mapMultipleUsers([userGame, userGame2])
    

    return gameDTO


def resume_game(game_id, user_id) :
    game = models.Game.objects.filter(id=game_id, players__id=user_id).first()
    if not game :
        raise NotPlayerError()

    gameDTO = mapGame(game)
    userGames = models.UserGame.objects.filter(game__id=game_id).all()
    gameDTO.players = mapMultipleUsers(userGames)
    return gameDTO


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

    if len(players) == 2 or (players and game.ias) :
        raise AlreadyTwoPlayerError()
    
    if not form.is_valid() :
        raise ColorInvalidError()
    hex_color = int(form.cleaned_data["hex_color"].replace("#", ""), 16)

    if hex_color == 0 :
        raise ForbidenColorError()
    if models.UserGame.objects.filter(game__id=game_id, color=hex_color).exists() :
        raise ColorAlreadyTakenError()
    
    models.UserGame.objects.create(userId=user, game=game, color=hex_color, userNumber=2)


# Entrainement des IA, (IA contre IA)
def train(self, ia_id, number_games) :
    ia = models.IA.objects.get(id=ia_id)
    players = list()
    posX = 0
    posY = 0
    for i in range(1, 3) :
        if i == 2 :
            posX = 7
            posY = 7

        players.append(IA(0, i, posX, posY, epsilon=ia.epsilonGreedy, learning_rate=ia.learningRate))

    game = Game(players) # ajout params en fonction du code de jordan(TODO)

    for game in range(number_games) : 
        game.init_board()
        while not game.game_over() :
            players[game.turn - 1].play(game)
            game.next_turn()
        
    ia.qtable = players[1].qTable
    ia.save()


def create_ia(form) :
    if not form.is_valid() :
        pass
    epsilon = form.cleaned_data["epsilonGreedy"]
    learningRate = form.cleaned_data["learningRate"]

    ia = models.IA.objects.create(epsilonGreedy=epsilon, learningRate=learningRate)

    return ia 


def list_ia_trainable() :
    ia_list = models.IA.objects.filter(qTable__isnull=True)
    return ia_list