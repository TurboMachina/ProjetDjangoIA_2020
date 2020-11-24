#_______________________________________________________________________________
# IA
#_______________________________________________________________________________

import numpy as np
from random import randint
import random
from game.DTO import Game
from game.DTO import User

class IA(User) : 

    def __init__(self, user_id, color, userNumber, posX, posY, epsilon=0.90, learning_rate=0.1) : # IA est un joueur, héritage
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
    
    @property
    def posX(self) : 
        return self.posX
    
    @property
    def posY(self) : 
        return self.posY
    


    
    # faire un mouvement en fonction de l epsilone greedy (decouverte ou pas)
    def take_action(state, Q, epsilon):
    if random.uniform(0, 1) < epsilon:
        action = randint(0, 3) # decouverte, random entre les 4 actions possible
    else: 
        action = np.argmax(Q[state]) # prendre le meilleur mouvement possible dans la table Q en fonction du state
    return action


    def move(self, action) : 
        self.posY = self.posY + self.actions[action][0]
        self.posX = self.posX + self.actions[action][1]

        return (self.posY, self.posX) , self.qtable[self._posY][self.posX] # retounr le state (unique) le reward associe 
    

    def play(game) :
        state =  (self.posY, self.posX) # state actuel ?

        action = self.take_action(state, self.qtable, self.epsilon) 

        nextState, reward = self.move(action)

        nextAction = self.take_action(nextState, self.qtable, 0.0) # La meilleure action

        qtable[state][action] = qtable[state][action] + self.learning_rate * (reward + self.epsilon * qtable[nextState][nextAction] - qtable[state][action])

    # Entrainement des IA, (IA contre IA)
    def train(self, ai1, ai2, number_games) :
        players = [ai1, ai2]
        game = Game(players)

        for game in range(number_games) : 
            play(game)
        

