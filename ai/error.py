#-----------------------------------------------------------------------------------------------
# Errors of the AI
#-----------------------------------------------------------------------------------------------

class Error(Exception) :
    pass

class NotValidAIError(Error) :
    def __init__(self) :
        self.message = "AI parameters are invalids"