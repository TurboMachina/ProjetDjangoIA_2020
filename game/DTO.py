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

    @posX.setter
    def posX(self, posX):
        self._posX = posX

    @posY.setter
    def posY(self, posY):
        self._posY = posY

    @property
    def userNumber(self) :
        return self._userNumber
    
    def to_json(self) :
        return self.__dict__

#_______________________________________________________________________________
# CLASS GAME
#_______________________________________________________________________________

class Game : 
    
    # Constructeur d'une game
    def __init__(self, id, gameState=None, turn=0, winner=None, players=[]):
        self._id = id
        self._gameState = gameState
        self._players = players
        self._col_size = 8 # Initialiser la taille des column à 8
        self._cells_left = self._col_size**2 # Initialiser le nombre de case non prise a 64 ou col_size^2
        self._turn = turn # Initialiser le tour a 0
        self._winner = winner


    # Getters utiles
    @property
    def id(self):
        return id

    @property
    def winner(self):
        return self._winner
    @winner.setter
    def winner(self, winner) :
        self._winner = winner

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
    
    def to_json(self) :
        return self.__dict__

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
        self.turn = self.turn % 2 + 1

    # Savoir si la game est finie
    def game_over(self) :
        for line in self.gameState :
            if 0 in line :
                return False
        return True
    def get_state1(self) : 
        return self.cells_left == 0
    
    def get_winner(self):
        points = {"1" : 0, "2" : 0}
        for line in self.gameState:
            for column in line:
                points[str(column)] = points[str(column)] + 1

        if points["1"] > points["2"]:
            return 1
        return 2

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
    # les coordonées utilisées par le système de lock_zone ne suivent pas les conventions du projet
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

            if not self.is_out_of_limits(nextx, nexty) and (nextx, nexty, False) not in cellsVisited and (nextx, nexty, True) not in cellsVisited and boards[nextx][nexty] != userNumber:  # on continue a chercher mais on arrive a un bord ou déjà fait
                if boards[nextx][nexty] == opponent:  # pas un enclos
                    cellsVisited.append((x, y, False))
                    return None

                self.find_won_block(boards, nextx, nexty, lookupTable, userNumber, opponent,cellsVisited)  # on continue a chercher

    def fillZone(self, boards, userNumber, cellVisited):
        to_be_filled = True
        for cell in cellVisited:
            if not cell[2]:
                to_be_filled = False
        if to_be_filled:
            for cell in cellVisited:
                boards[cell[0]][cell[1]] = userNumber

    def possible_actions(self, posX, posY, playerNumber) :
        actions = list()
        for action in [[0, 1], [0, -1], [1, 0], [-1, 0]] :
            if self.movement_ok({"x" : posX + action[0], "y" : posY + action[1]}, playerNumber) :
                actions.append(action)
        return actions