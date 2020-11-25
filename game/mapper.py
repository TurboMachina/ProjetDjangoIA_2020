from game.DTO import *

def mapUser(userGame) :
    return User(userGame.userId.id,
                userGame.userId.username,
                userGame.color,
                userGame.posUserX,
                userGame.posUserY,
                userGame.userNumber)

def mapMultipleUsers(userGames) :
    return [mapUser(userGame) for userGame in userGames]


def mapGame(game) :
    return Game(game.id, game.gameState, game.currentUser, game.winner)