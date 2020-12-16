from django.db.models import Count, Q

from game.DTO import *
import random
import game.models as models
from game.error import *
from game.mapper import *
from ai.business import play

def random_user_number() : 
    return random.randint(1,2)

#_______________________________________________________________________________
# FONCTION PRINCIPALE POUR JOUER
#_______________________________________________________________________________


def ia_plays(userGame, iaDTO, game, gameDTO) :
    userGame.move()
    if game.game_over() :
        gameDTO.winner = gameDTO.get_winner()
    gameDTO.next_turn() # TODO recup le move et mettre à jour le userGame


def maj_pos(newPosX, newPosY, gameDTO) :
    if not gameDTO.movement_ok({"x" : newPosX, "y" : newPosY}, gameDTO.turn) :
            raise InvalidMoveError()
        
    gameDTO.update_board(gameDTO.turn, {"posX" : newPosX, "posY" : newPosY})
    if gameDTO.game_over() :
        gameDTO.winner = gameDTO.get_winner()
    gameDTO.next_turn()


def move(userGame, moveX, moveY, gameDTO) :
    newPosX = userGame.posUserX + moveX
    newPosY = userGame.posUserY + moveY

    maj_pos(newPosX, newPosY, gameDTO)
    
    return (newPosX, newPosY)


def save_userGame(userGame, newPosX, newPosY) :
    userGame.posUserX = newPosX
    userGame.posUserY = newPosY
    userGame.save()


def save_game_state(game, gameDTO) :
    game.gameState = gameDTO.gameState
    game.currentUser = gameDTO.turn
    game.winner = gameDTO.winner
    game.save()


def save_move(userGame, newPosX, newPosY, game, gameDTO) :
    save_userGame(userGame, newPosX, newPosY)

    save_game_state(game, gameDTO)


def assign_pos(userGame, posX, posY=None) :
    if not posY :
        posY = posX
    userGame.posUserX = posX
    userGame.posUserY = posY

def assign_duo(userGame1, userGame2) :
    assign_pos(userGame1, 0)
    assign_pos(userGame2, 7)

def start_game(game_id, user) :
    games = models.Game.objects.annotate(Count("players"))
    games = games.annotate(Count("ia"))
    game = games.filter(id=game_id, players__id=user.id, gameState__isnull=True & Q(Q(players__count=2) | Q(players__count=1, ia__count=1))).first()
    if not game :
        raise StartGameError()
    
    gameDTO = Game(game_id)
    gameDTO.init_board()
    gameDTO.turn = random_user_number()

    save_game_state(game, gameDTO)

    userGames = models.UserGame.objects.filter(game__id=game.id)
    """
    for userGame in userGames :
        if userGame.userNumber == 1 :
            assign_pos(userGame, 0)
        elif userGame.userNumber == 2 :
            assign_pos(userGame, gameDTO.col_size - 1)
        if userGame.ia and userGame.userNumber == game.currentUser :
            ia_plays(userGame, mapIA(userGame), game, gameDTO) # TODO modifier appel de l'ia
        userGame.save()
    """
    if (userGames[0].userNumber == 1) :
        assign_duo(userGames[0], userGames[1])
        userGame1, userGame2 = userGames[0], userGames[1]
    else :
        assign_duo(userGames[1], userGames[0])
        userGame1, userGame2 = userGames[1], userGames[0]

    if userGame2.ia and userGame2.userNumber == gameDTO.turn :
        (moveX, moveY) = play(userGame1.posUserX, userGame1.posUserY, userGame2.posUserX, userGame2.posUserY, gameDTO.gameState, userGame2, gameDTO.possible_actions(userGame2.posUserX, userGame2.posUserY, userGame2.userNumber))
        (newPosX, newPosY) = move(userGames[1], moveX, moveY, gameDTO)
        save_move(userGames[1], newPosX, newPosY, game, gameDTO)
    
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
        (newPosX, newPosY) = move(userGame, movement["x"], movement["y"], gameDTO)
        
        userGame2 = models.UserGame.objects.filter(game__id=game.id).exclude(userId__id=user.id).first()
        if userGame2.ia and not gameDTO.game_over():
            (moveX, moveY) = play(userGame.posUserX, userGame.posUserY, userGame2.posUserX, userGame2.posUserY, gameDTO.gameState, userGame2, gameDTO.possible_actions(userGame2.posUserX, userGame2.posUserY, userGame2.userNumber))
            (newPosXAi, newPosYAi) = move(userGame2, moveX, moveY, gameDTO)
            save_userGame(userGame2, newPosXAi, newPosYAi)

        save_move(userGame, newPosX, newPosY, game, gameDTO)

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


def verrification_before_join(label, form, game_id) :
    game = models.Game.objects.get(id=game_id)

    players = game.players.all()

    if len(players) == 2 or (players and game.ias) :
        raise AlreadyTwoPlayerError()
    
    if not form.is_valid() :
        raise ColorInvalidError()
    hex_color = int(form.cleaned_data[label].replace("#", ""), 16)

    if hex_color == 0 :
        raise ForbidenColorError()
    if models.UserGame.objects.filter(game__id=game_id, color=hex_color).exists() :
        raise ColorAlreadyTakenError()
    
    return (game, hex_color)


def join_ia(game_id, ia_id, form) :
    game, hex_color = verrification_before_join("ia_color", form, game_id)

    ai = ai.models.AI.objects.filter(id=ia_id).first()

    models.UserGame.objects.create(ia=ai, game=game, color=hex_color, userNumber=2)


def join_game(game_id, user, form) :
    game, hex_color = verrification_before_join("hex_color", form, game_id)
    
    if user in game.players.all() :
        raise AlreadyPlayerError()
    
    models.UserGame.objects.create(userId=user, game=game, color=hex_color, userNumber=2)


# Entrainement des IA, (IA contre IA)
"""
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
def train(self, ia1, ia2, number_games) :
    players = [ia1, ia2]
    game = Game(players) # ajout params 

    for game in range(number_games) : 
        game.init_board()
        while not game.game_over() :
            players[game.turn - 1].play(game)
            game.next_turn()
        
    ia.qtable = players[1].qTable
    ia.save()

"""