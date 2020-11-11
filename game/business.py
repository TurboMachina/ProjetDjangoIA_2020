from DTO.game import Game
from DTO.game import UserGame
import random


# Joueur random pour debuter game
def random_user_number() : 
    return random.randint(1,2)

def play(game) : 

    # Initiallisation du board
    game.init_board()

    players = game.UserGames # Recuperation des deux joueurs sous forme dun tableau

    game.userNumber = random_user_number() # obtenir le numero du joueur qui commence 1 ou 2

    while(game.get_state() != -1) : # boucle tant que toutes les cases ne sont pas prises

        game.print_board()
        movement = players[game.userNumber].play() # demande de jouer

        if(movement_ok(movement)) : # verification que le movement est possible (reprend plusieurs fonctions)
            players[game.userNumber].move(movement) # le joueur bouge d'une case
            game.update_board() # update le board = changer le state (sans l'afficher)

            game.userNumber = game.next_turn(turn) # change de tour
            
        else : 
            print_error() # afficher message erreur car mouvement pas possible
    

    game.print_result()






