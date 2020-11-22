#_______________________________________________________________________________
# IA
#_______________________________________________________________________________

# J'ai créé un fichier à part pour l'IA car je savais pas trop ou la mettre (TODO) 

import numpy as np
from random import randint
import random
from game.DTO import Game
from game.DTO import UserGame
from game.DTO import User

class IA(User) : 

    def __init__(self, user_id, color, userNumber, posX, posY, epsilon=0.90, learning_rate=0.1,) : # IA est un joueur, héritage
        User.__init__(self, user_id, color, userNumber, posX, posY)
        self._epsilon = epsilon
        self._learning_rate = learning_rate
        self._qtable = []
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
    def learning_rate(self):
        return self._learning_rate

    @property
    def qtable(self) : 
        return self._qtable


    
    # faire un mouvement en fonction de l epsilone greedy (decouverte ou pas)
    def take_action(self, state, Q, epsilon):
        if random.uniform(0, 1) < epsilon:
            action = randint(0, 3) # decouverte, random entre les 4 actions possible
        else: 
            action = np.argmax(Q[state]) # prendre le meilleur mouvement possible dans la table Q en fonction du state
        return action

    def move(self, action) : 
        self._posY = self._posY + self.actions[action][0]
        self._posX = self._posX + self.actions[action][1]

        return (self.y + self.x) , self.qtable[self._posY][self._posX] # ! quand on retourne le state, il doit etre unique pour chaque case (0-64) TODO
    

    def play(self, game, state) :
        # state =  recuperer x - y et les transformer pour qu'ils soit entre 0 et 64 TODO

        action = move(state, self.qtable, self.epsilon)

        nextState, reward = move(action)

        nextAction = move(nextState, self.Q, 0.0)

        qtable[state][action] = Q[state][action] + self.learning_rate * (reward + self.epsilon * Q [nextState][nextAction] - Q[state][action])

    
    def train(self) : 
        pass

