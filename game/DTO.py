# -----------------------------------------------------------------------------------------------
# DTO for the game
# -----------------------------------------------------------------------------------------------

# ------------------------------------------------ GAME ----------------------------------------------------------
class User:

    def __init__(self, user_id, username, color, pos_x, pos_y, user_number):
        self._id = user_id
        self._username = username
        self._color = "#{0:06x}".format(color)
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._user_number = user_number

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
    def pos_x(self):
        return self._pos_x

    @property
    def pos_y(self):
        return self._pos_y

    @pos_x.setter
    def pos_x(self, pos_x):
        self._pos_x = pos_x

    @pos_y.setter
    def pos_y(self, pos_y):
        self._pos_y = pos_y

    @property
    def user_number(self):
        return self._user_number

    def to_json(self):
        return self.__dict__


# ------------------------------------------------ GAME ----------------------------------------------------------
class Game:

    def __init__(self, id, game_state=None, turn=0, winner=None, players=None):
        if players is None:
            players = []
        self._id = id
        self._game_state = game_state
        self._players = players
        self._col_size = 8  # Initialiser la taille des column à 8
        self._cells_left = self._col_size ** 2  # Initialiser le nombre de case non prise a 64 ou col_size^2
        self._turn = turn  # Initialiser le tour a 0
        self._winner = winner

    @property
    def id(self):
        return id

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, winner):
        self._winner = winner

    @property
    def game_state(self):
        return self._game_state

    @game_state.setter
    def game_state(self, game_state):
        self._game_state = game_state

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
    def turn(self, turn):
        if 0 < turn <= 2:
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

    def to_json(self):
        return self.__dict__

    # ------------------------------------------------ MAIN LOGIC OF A GAME ----------------------------------------------------------

    def init_board(self):
        game_state = list()
        for _ in range(self.col_size):
            line = list()
            for _ in range(self.col_size):
                line.append(0)
            game_state.append(line)

        game_state[0][0] = 1
        game_state[self.col_size - 1][self.col_size - 1] = 2

        self.cells_left -= 2
        self.game_state = game_state

    def next_turn(self):
        self.turn = self.turn % 2 + 1

    def game_over(self):
        for line in self.game_state:
            if 0 in line:
                return False
        return True

    def get_state1(self):
        return self.cells_left == 0

    def get_winner(self):
        points = {"1": 0, "2": 0}
        for line in self.game_state:
            for column in line:
                points[str(column)] = points[str(column)] + 1

        if points["1"] > points["2"]:
            return 1
        return 2

    def update_current_cells(self, x, y, turn):
        self.game_state[x][y] = turn

    def update_board(self, user_number, position):
        self.update_current_cells(position["posX"], position["posY"], user_number)
        self.lock_won_block(self.game_state, position["posX"], position["posY"], user_number)

    # --------------------------------------- LOGIC TO CHECK IF A MOVE IS POSSIBLE --------------------------------------------------

    # On avance en dehors du tableau
    def is_out_of_limits(self, x, y):
        return x < 0 or x >= self.col_size or y < 0 or y >= self.col_size

    def cell_already_taken(self, x, y, turn):
        return (self.game_state[x][y] != turn and self.game_state[x][y] != 0)
        # function qui regarde si il ne va pas sur une case de ladversaire

    def movement_ok(self, movement, turn):
        return not self.is_out_of_limits(movement["x"], movement["y"]) and not self.cell_already_taken(movement["x"],
                                                                                                       movement["y"],
                                                                                                       turn)

    # fonction qui vérifie et update un bloc de cases capturées
    # x et y = position prise par le joueur UserNumber
    # les coordonées utilisées par le système de lock_zone ne suivent pas les conventions du projet
    def lock_won_block(self, boards, x, y, user_number):
        lookup_table = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        opponent = user_number % 2 + 1
        directionnal_cells = [[], [], [], []]
        direction = 0
        for look in lookup_table:
            nextx = x + look[0]
            nexty = y + look[1]
            if (not self.is_out_of_limits(nextx, nexty)) and boards[nextx][nexty] == 0:
                self.find_won_block(boards, nextx, nexty, lookup_table, user_number, opponent,
                                    directionnal_cells[direction])
                self.fill_zone(boards, user_number, directionnal_cells[direction])
                direction += 1

    def find_won_block(self, boards, x, y, lookup_table, user_number, opponent, cells_visited):
        for look in lookup_table:
            next_x = x + look[0]
            next_y = y + look[1]

            cells_visited.append((x, y, True))

            if not self.is_out_of_limits(next_x, next_y) and (next_x, next_y, False) not in cells_visited and (
                    next_x, next_y, True) not in cells_visited and boards[next_x][
                next_y] != user_number:  # on continue a chercher mais on arrive a un bord ou déjà fait
                if boards[next_x][next_y] == opponent:  # pas un enclos
                    cells_visited.append((x, y, False))
                    return None

                self.find_won_block(boards, next_x, next_y, lookup_table, user_number, opponent,
                                    cells_visited)  # on continue a chercher

    def fill_zone(self, boards, user_number, cell_visited):
        to_be_filled = True
        for cell in cell_visited:
            if not cell[2]:
                to_be_filled = False
        if to_be_filled:
            for cell in cell_visited:
                boards[cell[0]][cell[1]] = user_number

    def possible_actions(self, pos_x, pos_y, player_number):
        actions = list()
        for action in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            if self.movement_ok({"x": pos_x + action[0], "y": pos_y + action[1]}, player_number):
                actions.append(action)
        return actions
