
# 0 = case non prise
# 1 = case prise par le joueur 1
# 2 = case prise par le joueur 2

#  x
# |
# |
# |______ y


class UserGame : 

    # Constructeur d'un UserGame
    def __init__(self, color, userNumber, posUserX, posUserY): 
        self._userNumber = userNumber # savoir si le user est 1 ou 2
        self._color = color
        self._posX = posUserX
        self._posY = posUserY
    
    # setters et getters ?
    
    # Demande à l'utilisateur son mouvement
    def play(self):
        # ask user to click on a button UP or DOWN or LEFT or RIGHT
        # Recuperer le mouvement

        return movement
    
    # Un mouvement
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

        return (x, y) # retourne les coordonées de la nouvelle case 
    
    


class Game : 
    
    # Constructeur d'une game
    def __init__(self, id, currentUser, gameState, userGames):
        self._id = id
        self._currentUser = currentUser
        self._gameState = gameState
        self._userGames = userGames
    
    # setters et getters ?
    
    # Initialisation board
    def _init_board(self):
        self._gameState = "1" + ("0" * (len(self.gameState) - 2)) + "2" # Mettre 1 en haut à gauche, 0 partout et 2 en bas à droite

    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y) : 
        if (x >= 0 and x < len(self.gameState)) and (y >= 0 and y < len(self.gameState)): # ? pas sur du len()
            return False

        return True

    # On change la case
    def update_cell(self, user, x, y) : 
        cell = # case x , y
        if(cell == "0") : 
            cell = user.userNumber
            user.
    
    # function qui regarde si il ne va pas sur une case de l'adversaire

    # function qui compte et remplit les cases prisent 

    # function qui affiche le tableau updated

    # function qui affiche le winner

    # function qui commence la game 
