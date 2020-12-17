class Error(Exception) :
    pass


class StartGameError(Error) :
    def __init__(self) :
        self.message = "you are not allow to start this game"


class NotPlayerError(Error) :
    def __init__(self) :
        self.message = "you are not a player of this game"


class GameNotStartedError(Error) :
    def __init__(self) :
        self.message = "this game is not started yet"



class NotYourTurnError(Error) :
    def __init__(self) :
        self.message = "this is not your turn"


class InvalidMoveError(Error) :
    def __init__(self) :
        self.message = "invalid move"


class AlreadyPlayerError(Error) :
    def __init__(self) :
        self.message = "you are already in this game"


class AlreadyTwoPlayerError(Error) :
    def __init__(self) :
        self.message = "there is already two players"

class ColorError(Error) :
    pass

class ColorInvalidError(ColorError) :
    def __init__(self) :
        self.message = "invalid color"

class ColorAlreadyTakenError(Error) :
    def __init__(self) :
        self.message = "this color is already taken"

class ForbidenColorError(ColorError) :
    def __init__(self) : 
        self.message = "this color is forbiden"


class NumberOfGameNotValid(Error) :
    def __init__(self) :
        self.message = "number of games is not valid"