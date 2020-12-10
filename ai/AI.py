import numpy as np
from random import randint
import random
from game.DTO import Game
from game.DTO import User
from game.models import UserGame


 """
#_______________________________________________________________________________
# CLASS STATE
#_______________________________________________________________________________

class State : 
    def __init__(self, idState, posXJ1, posXJ2, posYJ1, posYJ2, gameState) : 
        self._idState = idState
        self._posXJ1 = posXJ1
        self._posXJ2 = posXJ2
        self._posYJ1 = posYJ1
        self._posYJ2 = posYJ2
        self._gameState = gameState
        self.moves = [
            [-1, 0], # Up
            [1, 0], #Down
            [0, -1], #Left
            [0, 1] #Right
        ]
        self.esperance = 
    
    @property
    def state(self):
        pass

#_______________________________________________________________________________
# CLASS IA
#_______________________________________________________________________________


class IA :
    def __init__(self, idIa, userGame, epsilon=0.1, learning_rate=0.5, gama=0.9, states=[]) : 
        self._idIa = idIa
        self._epsilon = epsilon
        self._learning_rate = learning_rate
        self._gama = gama
        self._states = states
        self._userGame = userGame

    @property
    def epsilon(self):
        return self._epsilon
    
    @property
    def gama(self):
        return self._gama

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def game(self):
        return self._game

    def initQTable(self):
        QT = []
        for _ in range(0, 64):
            QT += [[0, 0, 0, 0]]
        return QT

    def initGame(self):
        game = Game(0, [], [1, 2])
        game.init_board()
        return game

    def move(self, action):
        self.posY = self.posY + self.actions[action][0]
        self.posX = self.posX + self.actions[action][1]

        p1 = 0
        p2 = 0
        for line in self.game.gameState:
            p1 += line.count(1)
            p2 += line.count(2)

        reward = p1 - p2

        return self.posY+1 + (self.posX+1)*8, reward # retoune le state (unique) le reward associe
    """


    # faire un mouvement en fonction de l epsilone greedy (decouverte ou pas)
    def take_action(self, state, game, epsilon):
        moves = [[-1, 0], # Up
                [1, 0], #Down
                [0, -1], #Left
                [0, 1]] #Right

        if random.uniform(0, 1) < epsilon:
            action = moves(randint(0, 3))
        else:
            bestEsperance = Esperance.objects.all().aggregate(Max('esperance')) # Pas sur que ca fonctionne ?
            action = Move.objects.get(id = bestEsperance.move)
            #action = np.argmax(qtable[state]) prendre le meilleur mouvement possible dans la table Q en fonction du state
        return action

    def reward(self, gameState) : 
        for line in gameState:
            nbCellsPlayer1 += line.count(1)
            nbCellsPlayer2 += line.count(2)
        return nbCellsPlayer1 - nbCellsPlayer2

    def play(self, stateId, posXUser1, posYUser1, posXUser2, posYUser2, game_sate):
        try : 
            state = State.objects.get(id = stateId, posXUser1 = posXUser1, posYUser1 = posYUser1, posXUser2 = posXUser2, posYUser2 = posYUser2, game_sate = game_sate)
        except SomeModel.DoesNotExist :
            state = None

        if state = None :
            state = State.objects.create(id = stateId, posXUser1 = posXUser1, posYUser1 = posYUser1, posXUser2 = posXUser2, posYUser2 = posYUser2, game_sate = game_sate)

        action = self.take_action(state, self.game, self.epsilon)

        try : 
            nextState = UserGame.objects.get(id=)
        except SomeModel.DoesNotExist :
            nextState = None

        reward = reward(game_state)
        
        nextAction = self.take_action(nextState, self.game, 0.0) 

        try : 
            esperanceBD = Esperance.objects.get(fk = state, fk = action)
        except SomeModel.DoesNotExist :
            esperanceBD = None

        esperance = Esperance.objects.get(fk = state, fk = action) + self.learning_rate * (reward + self.gama * Esperance.objects.get(fk = nextState, fk = nextAction) - Esperance.objects.get(fk = state, fk = action))

        if esperanceBD = None :
            esperanceBD = Esperance.objects.create(fk = state, fk = action, esperance = esperance)
        else : 
            #esperanceBD = modifier esperance dans la BD TODO





        # state = self.posY+1 + (self.posX+1)*8 # position dans le board
        # nextState, reward = self.move(action)
        #self.qtable[state][action] = self.qtable[state][action] + self.learning_rate * (reward + self.gama * self.qtable[nextState][nextAction] - self.qtable[state][action])

