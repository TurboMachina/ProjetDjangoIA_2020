# -----------------------------------------------------------------------------------------------
# Errors of the game
# -----------------------------------------------------------------------------------------------

class Error(Exception):
    def __init__(self):
        self.message = "Error rendering the page"


class StartGameError(Error):
    def __init__(self):
        self.message = "You are not allowed to start this game"


class NotPlayerError(Error):
    def __init__(self):
        self.message = "You are not a player of this game"


class GameNotStartedError(Error):
    def __init__(self):
        self.message = "tThis game is not started yet"


class NotYourTurnError(Error):
    def __init__(self):
        self.message = "It is not your turn"


class InvalidMoveError(Error):
    def __init__(self):
        self.message = "Invalid move"


class AlreadyPlayerError(Error):
    def __init__(self):
        self.message = "You are already in this game"


class AlreadyTwoPlayerError(Error):
    def __init__(self):
        self.message = "There is already two players"


class ColorError(Error):
    def __init__(self):
        self.message = "Error color"


class ColorInvalidError(ColorError):
    def __init__(self):
        self.message = "Invalid color"


class ColorAlreadyTakenError(Error):
    def __init__(self):
        self.message = "This color is already taken"


class ForbidenColorError(ColorError):
    def __init__(self):
        self.message = "This color is forbiden"


class NumberOfGameNotValid(Error):
    def __init__(self):
        self.message = "The number of games is not valid"
