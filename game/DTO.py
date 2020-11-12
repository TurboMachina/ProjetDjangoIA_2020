

#_______________________________________________________________________________
# CLASS USERGAME
#_______________________________________________________________________________

class UserGame : 

    # Constructeur d'un UserGame
    def __init__(self, color, userNumber, posUserX, posUserY): 
        self._userNumber = userNumber # savoir si le user est 1 ou 2
        self._color = color
        self._posX = posUserX
        self._posY = posUserY
    
    # setters et getters ?
    
# --------------------- METHODES GENERALEs DU JOUEUR ---------------------

    # Demande à l'utilisateur son mouvement
    def play(self):
        # ask user to click on a button UP or DOWN or LEFT or RIGHT
        # Recuperer le mouvement

        return movement
    
    # Appliquer le mouvement 
    def move(self, movement):
        if movement == "UP":
            x = self._posX
            y = self._posY - 1

        elif movement == "DOWN":
            x = self._posX
            y = self._posY + 1

        elif movement == "LEFT":
            x = self._posX - 1
            y = self._posY

        elif movement == "RIGHT":
            x = self._posX + 1
            y = self._posY 

        return (x, y) # retourne les coordonees de la nouvelle case 
    
    

#_______________________________________________________________________________
# CLASS GAME
#_______________________________________________________________________________


class Game : 
    
    # Constructeur d'une game
    def __init__(self, id, currentUser, gameState, userGames):
        self._id = id
        self._currentUser = currentUser
        self._gameState = gameState
        self._userGames = userGames
    
    # setters et getters ?
    

# --------------------- METHODES GENERALEs AU JEU ---------------------

    # Initialisation board
    def init_board(self):
        # Mettre 1 en haut a gauche, 0 partout et 2 en bas a droite
        gameStateInt = "1" + ("0" * (len(self.gameState) - 2)) + "2" 
        self._gameState = [int(x) for x in str(gameStateInt)] 

    # Passe au joueur suivant
    def next_turn(turn) :
        if(turn == 1) : 
            return 2
        return 1

    def get_state(self, gameState) : 
        # Savoir si toutes les cases sont prises, retourner -1 si c'est le cas

    # On change la case
    def update_cell(self, user, x, y) : 
        cell = # case x , y
        if(cell == "0") : 
            cell = user.userNumber
    
    # Game done ?
    def get_state(self, gameState) : 
        # parcourir le tableau et voir si toutes les cases sont prises

    def print_results() : 
        # Afficher gagnant 

    def update_board(self, player, movement) : 
        new_position_xy = player.move(movement)
        # function qui update le board
    

    # function qui compte et remplit les cases prisent 



# --------------------- METHODES VERIFIANT SI LE MOVEMENT EST OK ---------------------
    
    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y) : 
        if (x >= 0 and x < len(self.gameState)) and (y >= 0 and y < len(self.gameState)): 
            return False
        return True
    
    def case_already_taken(movement) : 
        # function qui regarde si il ne va pas sur une case de ladversaire

    def movement_ok(movement) : 
        if(!(is_out_of_limits(movement))) : 
            if(!(case_already_taken(movement))) : 
                return True
        return False
    
    def print_error() : 
        # Afficher erreur car mouvement impossible 



