# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 15:52:30 2021

@author: Owen
"""
from random import randrange
from ale_py import ALEInterface
import sys
import openpyxl
import pandas as pd
import numpy as np
from PIL import Image
import pandas as pd

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


file=[]
ram=[]
for i in range(3000):
    a=str(i)
    file.append(a+'.png')
    
    



# This strategy is to let the board move with the ball by comparing their y-positions. 

act=0   
for frame in range (3000):
    a=action(act)
    image=a[0]
    ale.saveScreenPNG(file[frame])
    image2=np.reshape(image,(210,160)) #flatten to 2d
    image2=image2[34:194,:] #eliminate white edges
    
    bkgd=image2[0,0] #bacground color
    
    #find where board is
    for row in range (len(image2[:,141])): 
        if(image2[row,141]==bkgd):
            continue
        else:
            board=row+7.5 # y-position of the centre of board
            break
    #find where ball is
    b=0
    for row in range (len(image2[:,0])):
        if(b==1):
            break
        for column in range (len(image2[0,20:141])):
            if(image2[row,column]==bkgd):
                ball=-1 #no ball
            else:
                ball=row+1.5 # y-position of the centre of board
                b=1
                break
    
    if(ball==-1):
        ball=board
    
    if(board>ball):
        act=1
    elif(board<ball):
        act=-1
    else:
        act=0
    #print(ball,board,act)
    