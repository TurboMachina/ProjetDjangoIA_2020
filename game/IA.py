#_______________________________________________________________________________
# IA
#_______________________________________________________________________________

# J'ai créé un fichier à part pour l'IA car je savais pas trop ou la mettre (TODO) 

import numpy as np
from random import randint
import random

class IA(UserGame) : 

    def __init__(self, user, color, userNumber, posUserX, posUserY, epsilon=0.90, learning_rate=0.1,) : # IA est un joueur, héritage
        UserGame.__init__(self, user, color, userNumber, posUserX, posUserY)
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
    # On modifie la function déjà présente dans le DTO pour un user normal
    def play(state, Q, epsilon):
    if random.uniform(0, 1) < epsilon:
        action = randint(0, 3) # decouverte, random entre les 4 actions possible
    else: 
        action = np.argmax(Q[state]) # prendre le meilleur mouvement possible dans la table Q en fonction du state
    return action
    

    def move() :
        # state = ? place initiale (TODO)
        # action = play(state, self.Q, self.epsilon)

        # move, reward = movement() (TODO)

        # atp1 = play(move, Q, 0.0)
        # update the Q function
        Q[state][action] = Q[state][action] + self.learning_rate * (reward + self.epsilon * Q [move][atp1] - Q[state][action])

        # Change the state
        # state = stp1

