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
    def id(self) :
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def color(self) :
        return self._color
    
    @property
    def posX(self) :
        return self._posX

    @property
    def posY(self) :
        return self._posY
    
    @property
    def userNumber(self) :
        return self._userNumber

#_______________________________________________________________________________
# CLASS GAME
#_______________________________________________________________________________

class Game : 
    
    # Constructeur d'une game
    def __init__(self, id, gameState=None, turn=0, players=[]):
        self._id = id
        self._gameState = gameState
        self._players = players
        self._col_size = 8 # Initialiser la taille des column à 8
        self._cells_left = self._col_size**2 # Initialiser le nombre de case non prise a 64 ou col_size^2
        self._turn = 0 # Initialiser le tour a 0


    # Getters utiles
    @property
    def id(self):
        return id

    @property
    def gameState(self):
        return self._gameState
    @gameState.setter
    def gameState(self, gameState) :
        self._gameState = gameState

    @property
    def cells_left(self):
        return self._cells_left
    @cells_left.setter
    def cells_left(self, cells_left):
        self._cells_left = cells_left

    @property
    def turn(self):
        return self._turn
    @turn.setter
    def turn(self, turn) :
        if turn > 0 and turn <= 2 :
            self._turn = turn

    @property
    def col_size(self):
        return self._col_size

    @property
    def players(self):
        return self._players
    @players.setter
    def players(self, players):
        self._players = players
    
    

# --------------------- METHODES GENERALEs AU JEU ---------------------

    # Initialisation board
    def init_board(self):
        gameState = list()
        for _ in range(self.col_size) :
            line = list()
            for _ in range(self.col_size) :
                line.append(0)
            gameState.append(line)

        gameState[0][0] = 1
        gameState[self.col_size - 1][self.col_size - 1] = 2
        
        self.cells_left -= 2
        self.gameState = gameState

    # Passe au joueur suivant (UserNumber est soit 1 soit 2)
    def next_turn(self) :
        self.turn = self.turn%2 + 1

    # Savoir si la game est finie
    def get_state1(self) :
        return 0 in self.gameState
    def get_state(self) : 
        return self.cells_left == 0
    
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

        if nbOne > nbTwo :
            # TODO : (faire un setter pour game state avec conditions ?) value userGame is unsubscriptable
            return self.players[0].user.username
        return self.players[1].user.username

    def update_current_cells(self, x, y, turn) :
        self.gameState[x][y] = turn
            # function qui remplit les cases prisent

    ### si elle prennait une position plutôt qu'un mouvement elle pourrait être utilisée dans lock_won_lock avec un for 
    ### 
    def update_board(self, userNumber, position) : 
        self.update_current_cells(position["posX"], position["posY"], userNumber)
        self.lock_won_block(self.gameState, position["posX"], position["posY"], userNumber)



# --------------------- METHODES VERIFIANT SI LE MOVEMENT EST OK ---------------------

    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y) : 
        return x < 0 or x >= self.col_size or y < 0 or y >= self.col_size
    
    def cell_already_taken(self, x, y, turn) :
        return (self.gameState[x][y] != turn and self.gameState[x][y] != 0)
        # function qui regarde si il ne va pas sur une case de ladversaire

    def movement_ok(self, movement, turn) :
        return not self.is_out_of_limits(movement["x"], movement["y"]) and not self.cell_already_taken(movement["x"], movement["y"], turn)

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
