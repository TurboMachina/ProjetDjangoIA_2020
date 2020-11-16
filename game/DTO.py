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
        pass
        # return movement
    
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
        self._cells_left = 64 # Initialiser le nombre de case non prise a 64
        self._turn = 0 # Initialiser le tour a 0
        self._col_size = 8 # Initialiser la taille des column à 8
    

    # Getters utiles

    def userGames(self):
        return self._userGames
    
    def gameState(self):
        return self._gameState
    
    def cells_left(self):
        return self._cells_left
    
    def turn(self):
        return self._turn
    
    def col_size(self):
        return self._col_size
    
    

# --------------------- METHODES GENERALEs AU JEU ---------------------

    # Initialisation board
    def init_board(self):
        gameStateInt = "1" + ("0" * (self.col_size) - 2) + "2" 
        self._gameState = [int(x) for x in str(gameStateInt)] 
        self._cells_left -= 2

    # Passe au joueur suivant (UserNumber est soit 1 soit 2)
    def next_turn(self, turn) :
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
                # TODO : (faire un setter pour game state avec conditions ?) value gameState is unsubscriptable
                if(self.gameState[x][y] == "1"):
                    nbOne = nbOne + 1
                else : 
                    nbTwo = nbTwo + 1

        if nbOne > nbTwo:
            # TODO : (faire un setter pour game state avec conditions ?) value userGame is unsubscriptable
            return self.userGames[0].user.username
        return self.userGames[1].user.username

    def update_cells(self) :
        pass
            # function qui remplit les cases prisent 

    # function qui update le board

    ### si elle prennait une position plutôt qu'un mouvement elle pourrait être utilisée dans lock_won_lock avec un for 
    ### 
    def update_board(self, player, movement) : 
        new_position_xy = player.move(movement)
        self.update_cells()

    # fonction qui vérifie et update un bloc de cases capturées
        # x et y = position prise par le joueur UserNumber
    def lock_won_block(self, gameState, userNumber, x, y):
        cellsToBlock = []
        self.search_cell(gameState, userNumber, x, y, cellsToBlock)
        for cell in cellsToBlock :
            gameState[cellsToBlock[cell]] = userNumber # TODO : a voir si le deballage est correct ici ? 

    def search_cell(self, gameState, userNumber, x, y, cellsToBlock):
        for i in range(-1,2,2) :
            for j in range(-1,2,2) :
                if(gameState[x+i][y+j] == userNumber or self.is_out_of_limits(x+i, y+j)): # on regarde une de nos case ou hors plateau
                    return False
                elif(gameState[x+i][y+j] != userNumber and gameState[x+i][y+j] != 0): # on regarde une case de l'adversaire
                    return True
                else: # on continue a chercher (gamestate[+i][+j] == 0)
                    result = self.search_cell(gameState, userNumber, x+i, y+j, cellsToBlock)
                    if(result == True):
                        cellsToBlock.append([x,y])
                    



# --------------------- METHODES VERIFIANT SI LE MOVEMENT EST OK ---------------------
    
    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y) : 
        if (x >= 0 and x < self.col_size) and (y >= 0 and y < self.col_size) : 
            return False
        return True
    
    def cell_already_taken(self, movement) :
        pass
        # function qui regarde si il ne va pas sur une case de ladversaire

    def movement_ok(self, movement) : # TODO : ici mouvement_ok prend un mouvement en paramètre mais is_out_of_limits prend x et y
        if(not(self.is_out_of_limits(movement))) : 
            if(not(self.cell_already_taken(movement))) : 
                return True
        return False



