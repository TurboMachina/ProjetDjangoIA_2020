#_______________________________________________________________________________
# IA
#_______________________________________________________________________________

import numpy as np
from random import randint
import random
from game.DTO import Game
from game.DTO import User

class IA(User):

    def __init__(self, user_id, username, color, userNumber, posX, posY, epsilon=0.1, learning_rate=0.5, gama=0.9): # IA est un joueur, héritage
        User.__init__(self, user_id, username, color, userNumber, posX, posY)
        self._username = "IA"
        self._epsilon = epsilon
        self._learning_rate = learning_rate
        self._gama = gama
        self._qtable = self.initQTable()
        self._game = self.initGame()
        self.actions = [
            [-1, 0], # Up
            [1, 0], #Down
            [0, -1], # Left
            [0, 1] # Right
        ]

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
    def qtable(self):
        return self._qtable

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

    def resetGame(self, game):
        game.init_board()

    # faire un mouvement en fonction de l epsilone greedy (decouverte ou pas)
    def take_action(self, state, game, qtable, epsilon):
        if random.uniform(0, 1) < epsilon:
            action = randint(0, 3) # decouverte, random entre les 4 actions possible
        else:
            action = np.argmax(qtable[state]) # prendre le meilleur mouvement possible dans la table Q en fonction du state
        return action



    # TODO même méthode existe deja dans business, pas de duplication, utiliser une seule méthode et l'adapter pour qu'elle renvoit le reward

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

    def play(self):

        # TODO State = positions des deux joueurs + la grille 

        state = self.posY+1 + (self.posX+1)*8 # position dans le board

        action = self.take_action(state, self.game, self.qtable, self.epsilon)

        # TODO faire jouer le joueur entre state et next state

        nextState, reward = self.move(action)

        nextAction = self.take_action(nextState, self.game, self.qtable, 0.0) # La meilleure action

        self.qtable[state][action] = self.qtable[state][action] + self.gama * (reward + self.epsilon * self.qtable[nextState][nextAction] - self.qtable[state][action])



    # TODO Modifier la BD pour qtable
    # TODO changer le business pour que l'IA s'entraine sur toutes les games
    # TODO faire une fonctions en plus pour entrainer IA
    # TODO Adapter views / templates

