# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 10:30:53 2021

@author: Kaiyu
"""
from random import randrange
from ale_py import ALEInterface
import sys
import openpyxl
import pandas as pd
import numpy as np

ale = ALEInterface()
ale.loadROM('pong.bin')
    
def action (x):
    '''
    This is a function to perform action and advance the game into next frame.
    
    Parameters:
            x(int): actions +1 -- up; 0 -- nothing; -1 -- down
            
    Return:
            gray(Array of unit8): grayscaled image matrix
            reward(int): +1 -- player wins; 0 -- still in progress; -1 -- computer wins
            gameover(bool): True -- game over; False -- still in progress
    '''
    if x==1:
        reward=ale.act(3)
    if x==0:
        reward=ale.act(0)
    if x==-1:
        reward=ale.act(4)  
    gray=ale.getScreenGrayscale()
    gameover=ale.game_over()
    return  gray,reward,gameover
