# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 15:06:55 2021

@author: Owen
"""
from random import randrange
from ale_py import ALEInterface
import sys
import openpyxl
import pandas as pd
import numpy as np

ale = ALEInterface()
ale.loadROM('pong.bin')

def locate (image):
    '''

    Parameters
    ----------
    image : ndarray(210,160,1)
        grayscale image of the game

    Returns
    -------
    ball : ndarray
        position of the ball
    board : float64
        y position of the board of the player

    '''
    
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
                ball_x=-1 #no ball
                ball_y=-1
            else:
                ball_y=row+1.5 # y-position of the centre of board
                ball_x=column+0.5
                b=1
                break
    ball=np.array([ball_x,ball_y])
    return ball,board    

def action (x):
    '''
    
    This is a function to perform action and advance the game into next frame.
    
    Parameters:
            x(int): actions +1 -- up; 0 -- nothing; -1 -- down
            
    Return:
            state(list): state of game before action. 
                [x and y positions of ball (ndarray), y position of board] 
            
            state_next(list): state of game after action.
                [x and y positions of ball (ndarray), y position of board, direction of ball]
                for direction -1 to the left, +1 to the right, 0 stay still
            
            reward(int): +1 -- player wins; 0 -- still in progress; -1 -- computer wins
            
            gameover(bool): True -- game over; False -- still in progress
            
    '''
    image=ale.getScreenGrayscale()
    ball_i,board_i=locate(image)
    
    if x==1:
        reward=ale.act(11)
    if x==0:
        reward=ale.act(0)
    if x==-1:
        reward=ale.act(12)
        
    image=ale.getScreenGrayscale()
    ball_f,board_f=locate(image)    
            
    gameover=ale.game_over()
    
    state=[ball_i,board_i]
    if (ball_f[0]-ball_i[0]<0):
        direction=-1
    elif (ball_f[0]-ball_i[0]>0):
        direction=1
    else:
        direction=0
    state_next=[ball_f,board_f,direction]
    
    return  state,state_next,reward,gameover
