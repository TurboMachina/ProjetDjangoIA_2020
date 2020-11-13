#_______________________________________________________________________________
# CLASS USER
#_______________________________________________________________________________

class User : 

    # Constructeur d'un User
    def __init__(self, user_id, username, password): 
        self._id = user_id 
        self._username = username
        self._password = password

    # Getters utiles

    def username(self):
        return self._username
    

#_______________________________________________________________________________
# CLASS USERGAME
#_______________________________________________________________________________

class UserGame : 

    # Constructeur d'un UserGame
    def __init__(self, user, color, userNumber, posUserX, posUserY): 
        self._user = user
        self._userNumber = userNumber # savoir si le user est 1 ou 2
        self._color = color
        self._posX = posUserX
        self._posY = posUserY
    
    # Getters utiles

    def user(self):
        return self._user

    def userNumber(self):
        return self._userNumber

    
# --------------------- METHODES GENERALEs DU JOUEUR ---------------------

    # Demande a lutilisateur son mouvement
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
    def __init__(self, id, gameState, userGames):
        self._id = id
        self._gameState = gameState
        self._userGames = userGames
        self._cells_left = 64 # Initialize le nombre de case non prise a 64
        self._turn = 0 # Initialize le tour a 0
    

    # Getters utiles

    def userGames(self):
        return self._userGames
    
    def gameState(self):
        return self._gameState
    
    def cells_left(self):
        return self._cells_left
    
    def turn(self):
        return self._turn
    
    

# --------------------- METHODES GENERALEs AU JEU ---------------------

    # Initialisation board
    def init_board(self):
        # Mettre 1 en haut a gauche, 0 partout et 2 en bas a droite
        gameStateInt = "1" + ("0" * (len(self.gameState) - 2)) + "2" 
        self._gameState = [int(x) for x in str(gameStateInt)] 
        self._cells_left -= 2

    # Passe au joueur suivant (UserNumber est soit 1 soit 2)
    def next_turn(turn) :
        if(turn == 1) : 
            return 2
        return 1

    # Savoir si la game est finie
    def get_state(self) : 
        if(self._cells_left == 0) : 
            return False
        return True
    
    def get_winner(self, gameState):
        nbOne = 0
        nbTwo = 0
        for x in range(len(self.gameState)): 
            for y in range(len(self.gameState)):
                if(self.gameState[x][y] == "1"):
                    nbOne = nbOne + 1
                else : 
                    nbTwo = nbTwo + 1

        if nbOne > nbTwo:
            return self.userGames[0].user.username
        return self.userGames[1].user.username
    
    def print_results() : 
        username = get_winner()
        # Afficher sur page HTML

    def update_cells(self) : 
            # function qui compte et remplit les cases prisent 

    # function qui update le board
    def update_board(self, player, movement) : 
        new_position_xy = player.move(movement)
        update_cells()



# --------------------- METHODES VERIFIANT SI LE MOVEMENT EST OK ---------------------
    
    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y) : 
        if (x >= 0 and x < len(self.gameState)) and (y >= 0 and y < len(self.gameState)): 
            return False
        return True
    
    def ccell_already_taken(movement) : 
        # function qui regarde si il ne va pas sur une case de ladversaire

    def movement_ok(movement) : 
        if(not(is_out_of_limits(movement))) : 
            if(not(cell_already_taken(movement))) : 
                return True
        return False
    
    def print_error() : 
        # Afficher erreur car mouvement impossible 



