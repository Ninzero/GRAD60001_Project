# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 15:26:43 2021

@author: Kaiyu
"""

#Play the game with random stratety 
#For each frame, we can obtain an RNG inmage and RAM.

from random import randrange
from ale_py import ALEInterface
import sys
ale = ALEInterface()
ale.loadROM('pong.bin')
# Get the list of legal actions
legal_actions = ale.getLegalActionSet()

file=[]
ram=[]
for i in range(300):
    a=str(i)
    file.append(a+'.png')

#Play 300 frames
reward=0
for i in range(300):
    
    a = legal_actions[randrange(len(legal_actions))]
    #a=legal_actions[int(3)]   # action 'up'
    # Apply an action and get the resulting reward
    reward+=ale.act(a)
    if i<58:
        continue
    ale.saveScreenPNG(file[i])
    print(a)
    ram.append(ale.getRAM())
ale.reset_game()

