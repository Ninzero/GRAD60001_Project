#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tensorflow as tf 
import numpy as np
import gym as gym
import matplotlib as plt 
import sys
import random
from datetime import datetime 
from DQN import DQN, update_state, learn

# Some hyperparameter
Max_experience = 50000
Min_experience = 5000
experience_memory_buffer = []
batch_size = 32
episode_number = 1000
gamma = 0.99
eps = 1
eps_step = 0.01
eps_min = 0.01
total_t = 0
update_target = 2000
K = 2
## create the game env here should return state which is the beginning graph

##
model = DQN(K, scope = "model") # save path should define in the package!
target_model = DQN(K, scope = "target_model")

#start session
with tf.session() as sess:
    model.set_session(sess)
    target_model.set_session(sess)
    # initialize the variable and load the variable
    sess.run(tf.global_variable_initializer())
    model.load()
    # in the training process we will copy the coef of model to target model so wo do not need to load for target model
    # fill the experience replay buffer
    for i in range(Min_experience):
        action = np.random.randint(0, K)
        ## input the action here return should be obs, reward, done(whether the game is over)
        
        ##
        next_state =  update_state(state, obv)
        experience_memory_buffer.append([state, action, reward, next_state, done])
        if done:
            ## initialize the game here
        
            ##
        else:
            state = next_state
            
# play the game and learn
for i in range(episode_number):
    ## initialize the game env here
    
    ##
    done = False
    while not done:
        # update the target model here
        if not(t%update_target):
            model.copy_from(model)
        action  = model.sample_action(state, eps)
        ## input the action here return should be obs, reward, done(whether the game is over)
        
        ##
         next_state =  update_state(state, obv)
        if len(experience_memory_buffer) >= Max_experience:
            experince_memory_buffer.remove(experince_memory_buffer[0])
            experience_memory_buffer.append([state, action, reward, next_state, done])
        else:
            experience_memory_buffer.append([state, action, reward, next_state, done])
        loss =learn(model, target_model, experience_replay_buffer, gamma, batch_size)
        eps = max(eps-eps_step, min_eps)
       
            
    
        

