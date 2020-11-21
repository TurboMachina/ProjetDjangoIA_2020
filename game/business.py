from django.db.models import Count

from game.DTO import *
import random
import game.models as models


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
        return { "template_link" : "game/errorPage.html", "context" : {"error_message" : "you are not allow to start this game"}}
    
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

    return {"template_link" : "game/game.html", "context" : {"game" : game}}


def apply_move(game_id, user, movement) :
    userGame = models.UserGame.objects.filter(game__id=game_id, userId__id=user.id).first()
    if not userGame :
        return {"template_link" : "game/errorPage.html", "context" : {"error_message" : "you're not a player of this game"}}
    
    if not userGame.game.gameState :
        return {"template_link" : "game/errorPage.html", "context" : {"error_message" : "the game is not started"}}
    
    if not userGame.userNumber == userGame.game.currentUser :
        return {"template_link" : "game/errorPage.html", "context" : {"error_message" : "this is not your turn"}}
    
    game = userGame.game
    gameDTO = Game(game.id, game.gameState, userGame, game.currentUser)
    print(userGame.posUserX)
    print(userGame.posUserY)
    newPosX = userGame.posUserX + movement["x"]
    newPosY = userGame.posUserY + movement["y"]
    if not gameDTO.movement_ok({"x" : newPosX, "y" : newPosY}, gameDTO.turn) :
        return {"template_link" : "game/errorPage.html", "context" : {"error_message" : "invalid move"}}
    
    gameDTO.update_board(gameDTO.turn, {"posX" : newPosX, "posY" : newPosY})
    gameDTO.next_turn()

    game.gameState = gameDTO.gameState
    game.turn = gameDTO.turn
    game.save()

    userGames = models.UserGame.objects.filter(game__id=game.id)
    players = []
    for userGame in userGames :
        players.append(User(userGame.userId.id,
                            userGame.userId.username,
                            userGame.color,
                            userGame.posUserX,
                            userGame.posUserY,
                            userGame.userNumber))
    gameDTO.players = players
    return gameDTO




def play(game):
        
    # If la game n'est pas en cours on initialise 
    if(not(game.gameState())) :
        game.init_board() # Initiallisation du board
        game.turn = random_user_number() # obtenir le numero du joueur qui commence 1 ou 2

    players = game.userGames # Recuperation des deux joueurs sous forme dun tableau

    game.print_board()
    # TODO : c'est quoi cette méthode play() ? et players
    movement = players[game.turn].play() # demande de jouer
    
    if(game.movement_ok(movement, players[game.turn])) : # verification que le movement est possible (reprend plusieurs fonctions)
        game.update_board(players[game.turn], movement) # update le board avec le movement du joueur et les cases prises
        game.turn = game.nextturn(game.turn) # change de tour

    else : 
        game.print_error() # afficher message erreur car mouvement pas possible (ENCORE A FAIRE)

    game.print_winner() # afficher le winner (ENCORE A FAIRE)


def launch_game():

    # Information a retouver grace au model BD ? 

    ######### pour tester

    player1 = models.User(1, "aherrent", "abcd")
    player2 = models.User(2, "abaert", "password")

    p1 = UserGame(player1, "red", 1, 3, 7)
    p2 = UserGame(player2, "yellow", 2, 4, 5)

    players = [p1, p2]

    #game = Game(game_id, currentUser, gameState, players)
    game = models.Game.objects.get(id=30)

    #########

    
    play(game)



