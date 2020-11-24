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

def play(game):
        
    # If la game n'est pas en cours on initialise 
    if(not(game.gameState())) :
        game.init_board() # Initiallisation du board
        game.turn = random_user_number() # obtenir le numero du joueur qui commence 1 ou 2

    players = game.users # Recuperation des deux joueurs sous forme dun tableau

    if(not isinstance(players[game.turn], IA)) :
        # demande au joueur de jouer (click bouton) (TODO)
        movement = players[game.turn].move()
        game.print_board()
    else : 
        movement = players[game.turn].play(game)

    if(game.movement_ok(movement, players[game.turn])) : # verification que le movement est possible (reprend plusieurs fonctions)
        game.update_board(players[game.turn], movement) # update le board avec le movement du joueur et les cases prises
        game.turn = game.nextturn(game.turn) # change de tour
    else : 
        game.print_error() # afficher message erreur car mouvement pas possible (TODO)

    game.print_winner() # afficher le winner (TODO)

"""
def launch_game():
    player1 = models.User(1, "aherrent", "abcd")
    player2 = models.User(2, "abaert", "password")

    p1 = UserGame(player1, "red", 1, 3, 7)
    p2 = UserGame(player2, "yellow", 2, 4, 5)

    players = [p1, p2]

    #game = Game(game_id, currentUser, gameState, players)
    game = models.Game.objects.get(id=30)
    play(game)
"""


def play_human(self, ai) : 
    # p1 = models.User() On recupere le joueur
    players = [p1, ai]

    game = Game(players) # ajout params en fonction du code de jordan(TODO)

    play(game)


# Entrainement des IA, (IA contre IA)
def train(self, ai1, ai2, number_games) :
    players = [ai1, ai2]
    game = Game(players) # ajout params en fonction du code de jordan(TODO)

    for game in range(number_games) : 
        play(game)
    





