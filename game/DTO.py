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
    @property
    def user_id(self):
        return self._id
    @property
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
    @property
    def user(self):
        return self._user
    @property
    def userNumber(self):
        return self._userNumber
    @userNumber.setter
    def userNumber(self, newUserNumber):
        if newUserNumber > 0:
            self._userNumber = newUserNumber

    # --------------------- METHODES GENERALEs DU JOUEUR ---------------------

     # Demande a lutilisateur son mouvement (TODO)
    def play(self):
        # ask user to click on a button UP or DOWN or LEFT or RIGHT
        # Recuperer le mouvement
        pass
        # return movement

    # Appliquer le mouvement 
    def move(self, movement):
        x = 0
        y = 0
        if movement == "UP":
            x = self._posX
            y = self._posY - 1

        elif movement == "DOWN":
            x = self._posX
            y = self._posY + 1

        elif movement == "LEFT":L
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
        self._col_size = 8 # Initialiser la taille des column à 8
        self._cells_left = self._col_size**2 # Initialiser le nombre de case non prise a 64 ou col_size^2
        self._turn = 0 # Initialiser le tour a 0


    # Getters utiles
    @property
    def userGames(self):
        return self._userGames
    @property
    def gameState(self):
        return self._gameState
    @property
    def cells_left(self):
        return self._cells_left
    @property
    def turn(self):
        return self._turn
    @property
    def col_size(self):
        return self._col_size



# --------------------- METHODES GENERALEs AU JEU ---------------------

    # Initialisation board
    def init_board(self):
        gameStateInt = "1" + ("0" * ((self.col_size) - 2)) + "2"
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

    def update_current_cells(self, x, y, turn) :
        self.gameState[x][y] = turn
            # function qui remplit les cases prisent

    # function qui update le board

    ### si elle prennait une position plutôt qu'un mouvement elle pourrait être utilisée dans lock_won_lock avec un for 
    ### 
    def update_board(self, player, movement) :
        new_position_xy = player.move(movement)
        self.update_current_cells(new_position_xy.x, new_position_xy.y, player.turn)
        self.lock_won_block(player.new_position_xy.x, new_position_xy.y)


# --------------------- METHODES VERIFIANT SI LE MOVEMENT EST OK ---------------------

    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y) :
        if (x >= 0 and x < self.col_size) and (y >= 0 and y < self.col_size) :
            return False
        return True

    def cell_already_taken(self, x, y, turn) :
        return (self.gameState[x][y] != turn and self.gameState[x][y] != 0)
        # function qui regarde si il ne va pas sur une case de ladversaire

    def movement_ok(self, movement, turn) :
        if(not(self.is_out_of_limits(movement.x, movement.y))) :
            if(not(self.cell_already_taken(movement.x, movement.y, turn))) :
                return True
        return False

        # fonction qui vérifie et update un bloc de cases capturées
        # x et y = position prise par le joueur UserNumber
    def lock_won_block(self, boards, x, y, userNumber):
        lookupTable = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        opponent = userNumber % 2 + 1
        directionnalCells = [[], [], [], []]
        direction = 0
        for look in lookupTable:
            nextx = x + look[0]
            nexty = y + look[1]
            if (not self.is_out_of_limits(nextx, nexty)) and boards[nextx][nexty] != 0:
                result = self.find_won_block(boards, x, y, lookupTable, userNumber, opponent, directionnalCells[direction])
                if not result:
                    self.fillZone(boards, userNumber, directionnalCells[direction])

    def find_won_block(self, boards, x, y, lookupTable, userNumber, opponent, cellsVisited):
        cellsVisited.append((x, y))
        for look in lookupTable:
            nextx = x + look[0]
            nexty = y + look[1]
            if self.is_out_of_limits(nextx, nexty) or (nextx, nexty) in cellsVisited:  # on continue a chercher mais on arrive a un bord ou déjà fait
                return False
            if boards[nextx][nexty] == opponent:  # pas un enclos
                return True
            else:
                result = self.find_won_block(boards, nextx, nexty, lookupTable, userNumber, opponent, cellsVisited)  # on continue a chercher

    def fillZone(self, boards, userNumber, cellVisited):
        for cell in cellVisited:
            if cell == True:
                boards[cell[0], cell[1]] = userNumber