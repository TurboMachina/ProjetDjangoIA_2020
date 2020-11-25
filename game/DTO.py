#_______________________________________________________________________________
# CLASS USER
#_______________________________________________________________________________

class User :

    # Constructeur d'un User
    def __init__(self, user_id, username, color, posX, posY, userNumber):
        self._id = user_id
        self._username = username
        self._color = "#{0:06x}".format(color)
        self._posX = posX
        self._posY = posY
        self._userNumber = userNumber

    # Getters utiles
    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def color(self):
        return self._color

    @property
    def posX(self):
        return self._posX

    @property
    def posY(self):
        return self._posY

    @property
    def userNumber(self):
        return self._userNumber
    

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
                if(self.gameState[x][y] == "1"):
                    nbOne = nbOne + 1
                else :
                    nbTwo = nbTwo + 1

        if nbOne > nbTwo:
            return self.userGames[0].user.username
        return self.userGames[1].user.username

    def update_current_cells(self, x, y, turn) :
        self.gameState[x][y] = turn
            # function qui remplit les cases prisent

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
        lookup_table = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        opponent = userNumber % 2 + 1
        directionnal_cells = [[], [], [], []]
        direction = 0
        for look in lookup_table:
            nextx = x + look[0]
            nexty = y + look[1]
            if (not self.is_out_of_limits(nextx, nexty)) and boards[nextx][nexty] == 0:
                self.find_won_block(boards, nextx, nexty, lookup_table, userNumber, opponent, directionnal_cells[direction])
                self.fillZone(boards, userNumber, directionnal_cells[direction])
                direction += 1

    def find_won_block(self, boards, x, y, lookupTable, userNumber, opponent, cellsVisited):
        for look in lookupTable:
            nextx = x + look[0]
            nexty = y + look[1]

            cellsVisited.append((x, y, True))
            
            if self.is_out_of_limits(nextx, nexty) or ((nextx, nexty, False) in cellsVisited or (nextx, nexty, True) in cellsVisited) or boards[nextx][nexty] == userNumber:  # on continue a chercher mais on arrive a un bord ou déjà fait
                return None

            if boards[nextx][nexty] == opponent:  # pas un enclos
                cellsVisited.append((x, y, False))
                return None

            self.find_won_block(boards, nextx, nexty, lookupTable, userNumber, opponent, cellsVisited)  # on continue a chercher

    def fillZone(self, boards, userNumber, cellVisited):
        to_be_filled = True
        for cell in cellVisited:
            if not cell[2]:
                to_be_filled = False
        if to_be_filled:
            for cell in cellVisited:
                boards[cell[0]][cell[1]] = userNumber