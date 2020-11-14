from game.DTO import Game
from game.DTO import UserGame
import random
import game.models as models

# Joueur random pour debuter game
def random_user_number() : 
    return random.randint(1,2)

#_______________________________________________________________________________
# FONCTION PRINCIPALE POUR JOUER
#_______________________________________________________________________________

def play(game) : 
        
    # If la game n'est pas en cours on initialise 
    if(not(game.gameState())) :
        game.init_board() # Initiallisation du board
        game.turn = random_user_number() # obtenir le numero du joueur qui commence 1 ou 2

    players = game.userGames # Recuperation des deux joueurs sous forme dun tableau

    game.print_board()
    movement = players[game.turn].play() # demande de jouer
    
    if(movement_ok(movement)) : # verification que le movement est possible (reprend plusieurs fonctions)
        game.update_board(players[game.turn], movement) # update le board avec le movement du joueur et les cases prises
        game.turn = game.nextturn(game.turn) # change de tour

    else : 
        print_error() # afficher message erreur car mouvement pas possible (ENCORE A FAIRE)

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



