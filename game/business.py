from DTO.game import Game
from DTO.game import UserGame
import random


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



#_______________________________________________________________________________
# FONCTION MAIN
#_______________________________________________________________________________


if __name__ == "__main__":

    # Information a retouver grace au model BD ? 
    player1 = UserGame(user, color, userNumber, posUserX, posUserY)
    player2 = UserGame(user, color, userNumber, posUserX, posUserY)

    players = [player1, player2]

    # Information a retouver grace au model BD ? 
    game = Game(game_id, currentUser, gameState, players)

    play(game)



