from random import randrange
from ale_py import ALEInterface
import sys
import openpyxl
import pandas as pd
import numpy as np


def locate (image, ale):

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
    ball=ball_y
    return ball,board

def Action (x,action_list,ball_p,ale):
    '''
    
    This is a function to perform action and advance the game into next frame.
    
    Parameters:
            x(int): actions 0 -- up; 1 -- nothing; 2 -- down
            
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
    ball_i,board_i=locate(image,ale)
    
    if x=="0":
        # move up
      reward = ale.act(4)
      if reward ==0:
            reward = ale.act(4)
            if reward ==0:
                reward = ale.act(4)
                if reward ==0:
                    reward = ale.act(4)

  
    if x=="1":
        # move down
      reward = ale.act(3)
      if reward ==0:
            reward = ale.act(3)
            if reward ==0:
                reward = ale.act(3)
                if reward ==0:
                    reward = ale.act(3)

  
  
    if x =="2":
        ale.act(0)
        reward = ale.act(0)
        
    image=ale.getScreenGrayscale()
    ball_f,board_f=locate(image,ale)    
            
    gameover=ale.game_over()
    
    # if (ball_f[0]-ball_i[0]<0):
    #     direction=-1
    # elif (ball_f[0]-ball_i[0]>0):
    #     direction=1
    # else:
    #     direction=0
    temp = [0,0]
    for i in range(len(action_list)):
        temp[i]=action_list[i]
    state=[ball_p,ball_i,board_i,temp]

    action_list.remove(action_list[0])
    action_list.append(x)
    state_next=[ball_i,ball_f,board_f,action_list]

    if reward == 0:
        done = False
    if reward == 1 or reward == -1:
        done = True
    
    return  state,state_next,reward*10,gameover,done

def check_game(gameover, gameover_time, ale):
    if gameover:
        ale.reset_game()
        gameover_time += 1

        
def performance(gameover_time, gameover, ale, model, score_list):
            if not(gameover_time% 50):
                score = 0
                ball_p = "-1"
                action_list = [2,2]
                ale.act(0)
                state,  next_state,reward, gameover,done = Action("2", action_list,ball_p,ale)
                ball_p = state[1]
                state = str(state)
                next_state = str(next_state)
                while not gameover:
                    action = model.eps_action(next_state)
                    
                    state, next_state, reward, gameover,done = Action(action,action_list ,ball_p,ale)
                    ball_p = state[1]
                    state = str(state)
                    next_state = str(next_state)
                    if done:
                        score += reward
                score_list.append(score)
                print(score)
                ale.reset_game()
                print("Has played ",gameover_time,"rounds")
            else:
                print("Has played ",gameover_time,"rounds")
            