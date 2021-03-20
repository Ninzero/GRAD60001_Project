from Q_table import Q_table
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from env import Action,  check_game, performance
from ale_py import ALEInterface
import sys
import openpyxl
# hyperparameters
Min_experience = 500
Max_experience = 500000
experience_replay_buffer = []
episode_number = 80000
eps_step = 0.0001
score_list = []
gameover_time = 0
measure_time = 0
action_list = [2,2]
model = Q_table(["0", "1"] ,eps = 0.9 ,eps_min = 0.01, gamma = 0.99, learning_rate = 0.01)
print("model is loading...")
model.load()
# explore the env and save the exlporation into the buffer
print(model.Q)
ale = ALEInterface()
ale.loadROM('pong.bin')
ale.act(0)
print("filling the buffer...")
done = False
ball_p = -1
for i in range(Min_experience):    
    action =  np.random.randint(0,2)
    action  = str(action)
    # Add function that takes action return belows
    state, next_state,reward, gameover, done = Action(action,action_list,ball_p,ale)
    ball_p = state[1]
    state = str(state)
    next_state = str(next_state)
    experience_replay_buffer.append([state, action, reward, next_state, done])
    if gameover:
        action_list = [2,2]
        ale.reset_game()
        gameover_time += 1
        print("Game Over and Has gameover", gameover_time, "times")
print("buffer has been filled...Begining to training...")
action_list  = [2,2]
ball_p = -1
ale.act(0)
state, next_state, reward, gameover, done = Action("2", action_list,ball_p,  ale)
next_state = str(next_state)
for j in range(episode_number):
    done = False
    print("start episode ", j)       
    while not done:
        action = model.eps_action(next_state)
        state, next_state, reward, gameover, done = Action(action,action_list, ball_p, ale)
        ball_p = state[1]
        state = str(state)
        next_state = str(next_state)
        if len(experience_replay_buffer) == Max_experience:
            experience_replay_buffer.remove(experience_replay_buffer[0])
            experience_replay_buffer.append([state, action, reward, next_state, done])
        else:
            experience_replay_buffer.append([state, action, reward, next_state, done])
        model.learn(experience_replay_buffer)
        model.eps = max(model.eps_min, model.eps - eps_step)
        if gameover:
            action_list = [2,2]
            ball_p = -1
            ale.reset_game()
            gameover_time += 1
            print("Game Over and Has gameover", gameover_time, "times")
            performance(gameover_time, gameover, ale, model, score_list)
            ale.act(0)
            state, next_state, reward, gameover, done = Action("2", action_list,ball_p, ale)
            next_state = str(next_state)
            print([state, next_state, reward, gameover, done])
    print("Finished episode ", j)
    print("eps =", model.eps)
    if not(j%100):
        print("Training finished.....Saving the Q_table......")
        model.save()
# Print the reward in each episode of training
plt.plot(range(len(score_list)), score_list, 'go-', label='score line', linewidth=0.5)


    






