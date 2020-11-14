from game.DTO import Game
from game.DTO import UserGame
import random
import game.models

# Joueur random pour debuter game
def random_user_number() : 
    return random.randint(1,2)

#_______________________________________________________________________________
# FONCTION PRINCIPALE POUR JOUER
#_______________________________________________________________________________

def play(game) : 

    # Initiallisation du board
    game.init_board()

    players = game.userGames # Recuperation des deux joueurs sous forme dun tableau

    game.turn = random_user_number() # obtenir le numero du joueur qui commence 1 ou 2

    while(not(game.get_state())) : # boucle tant que toutes les cases ne sont pas prises

        game.print_board()
        movement = players[game.turn].play() # demande de jouer

        if(movement_ok(movement)) : # verification que le movement est possible (reprend plusieurs fonctions)
            game.update_board(players[game.turn], movement) # update le board avec le movement du joueur et les cases prises
            game.turn = game.nextturn(game.turn) # change de tour

        else : 
            print_error() # afficher message erreur car mouvement pas possible
    

    game.print_result()


def launch_game():

    # Information a retouver grace au model BD ? 

    player1 = User(user_id, username, password)
    player2 = User(user_id, username, password)

    p1 = UserGame(player1, color, userNumber, posUserX, posUserY)
    p2 = UserGame(player2, color, userNumber, posUserX, posUserY)

    players = [p1, p2]

    #game = Game(game_id, currentUser, gameState, players)
    game = Game.objects.get(id=game_id)

    play(game)



