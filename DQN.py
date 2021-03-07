#!/usr/bin/env python
# coding: utf-8

# In[43]:


import tensorflow as tf 
import numpy as np
import gym as gym
import matplotlib as plt 
import sys
import random
from datetime import datetime 

# hyperparameter
Image_size = "to be determined"
K = 2

class DQN:
    def __init__(self, K, scope, save_path = ""):
        self.K = K
        self.scope = scope
        self.save_path = save_path
        with tf.variable_scope(scope):
            # imput&target
            # use place holder to restore training data
            self.X = tf.placeholder(tf.float32, shape = (None, 2, Image_size, Image_size), name = "X")
            self.target_q_value = tf.placeholder(tf.float32, shape = (None,), name = "G")
            self.actions = tf.placeholder(tf.int32, shape = (None,), name = "action")
            Z = tf.transpose(X, (0,2,3,1))
           # building CNN
            cnn_L1 = tf.contrib.layers.conv2d(Z, filter, strides, padding, activation_fn = tf.nn.relu)
            cnn_L2 = tf.contrib.layers.conv2d(cnn_L1, filter, strides, padding, activation_fn = tf.nn.relu)
            cnn_L3 = tf.contrib.layers.conv2d(cnn_L2, filter, strides, padding, activation_fn = tf.nn.relu)
            fl = tf.contrib.layers.flatten(cnn_L3)
            fcn_L2= tf.contrib.layers.fully_connected(fl,filter_number)
           # Output layer
            self.predicted_action = tf.contrib.layers.fully_connected(fcn_L2, K)
            action_values = tf.reduce_sum(self.predicted_action * tf.one_hot(self.actions,K),reduction_indices=[1])
            self.cost = tf.reduce_mean(tf.square(self.target_q_value - action_values))
            self.train_op = tf.train.AdamOptimizer().minimize(self.cost)
    
    def set_session(self, session):
    # can be used to start a tf session
        self.session = session
        
    def predict(self, states):
    # predict the action based on the input
        return self.session.run(self.predict_action, feed_dict=({self.X: states}))

    def update(self, states, action, targets):
    # input the training data target Q value and update network
        c = self.session.run([self.cost, self.train_op],
                            feed_dict = {
                                self.X : states,
                                self.target_q_value : target,
                                self.actions : action
                            })
        return c

    def sample_action(self, x, eps):
    # sigma-greedy algorithm to select action
        if np.random.random()<eps:
            return np.random.choice(self.K)
        else:
            return np.argmax(self.predict([x])[0])
                                
    def copy_from(self, other):
    # copying the variable value from main model to target model only used by target network
        current_model_coef = [t for t in tf.trainable_variables() if  t.name.stratwith(self.scope)]
        current_model_coef = sorted(current_model_coef, key = lambda v:v.name)
        others = [t for t in tf.trainable_variables() if  t.name.stratwith(self.scope)]
        others = sorted(others, key = lambda v:v.name)
        ops = []
        for p, q in zip(current_model_coef, others):
                actual = self.session.run(q)
                op = p.assign(actual)
                ops.append(op)
        self.session.run(ops)
        
    def load(self):
        self.saver = tf.train.Saver(tf.global_variables())
        try:
            save_dir = '/'.join(self.save_path.split('/')[:-1])
            ckpt =tf.train.get_checkpoint_state(save_dir)
            load_path = ckpt.model_chackpoint_path
            self.saver.restore(self.session, load_path)
        except:
            print("no saved model to load. Starting new session")
        else:
            print("load model from: {}".format(load_path))
            saver = tf.train.Saver(tf.global_variables())
            episode_number = int(load_path.split('-')[-1])
            
        
    def save(self, n):
        self.saver.save(self.session, self.save_path, global_step=n)
        print("Svaed model {}".format(n))
        
        
        

def update_state(state, obv):
# this function is for appending obv on the channel
    return np.append(state[1:], np.expand(obv, 0), axis=0)

def learn(model, target_model, experience_replay_buffer, gamma, batch_size):
    # update the network by the above "update" function and return the value of loss function that can be used to reflect the progress of the training
        samples = random.sample(experience_replay_buffer, batch_size)
        states, actions, rewards, next_states, dones = map(np.array, zip(*samples))
        next_qs = target_model.predict(next_states)
        next_q = np.amax(next_qs, axis = 1)
        targets = rewards + np.invert(dones).astpye(float32)*gamma*next_q
        loss = model.update(states, actions, target)
        return loss
    
                                
    

