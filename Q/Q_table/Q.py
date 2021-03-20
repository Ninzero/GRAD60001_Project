import numpy as np
import pandas as pd
import random
class Q_table:
    def __init__(self, action_type ,eps = 0.99 ,eps_min = 0.01, gamma = 0.99, learning_rate = 0.05):
        self.actions = action_type
        self.Q = pd.DataFrame(columns=self.actions, dtype=np.float64)
        self.gamma = gamma
        self.eps = eps
        self.eps_min = eps_min
        self.rate = learning_rate

    def eps_action(self, state):
        if state not in self.Q.index:
            # append new state to q table
            self.Q = self.Q.append(pd.Series([0]*len(self.actions), index=self.Q.columns, name=state))
            action = np.random.randint(0,2)

            return str(action)
        if np.random.random() < self.eps:
            action = np.random.randint(0,2)

            return str(action)
        else:
            Q_values = self.Q.loc[state, :]
            action  = np.argmax(Q_values)

            return str(action)

    def learn(self, experience_replay_buffer): 
            samples = random.sample(experience_replay_buffer, 1)
            state = samples[0][0]
            action = samples[0][1]
            reward = samples[0][2]
            next_state = samples[0][3]
            done = samples[0][4]
            if state not in self.Q.index:
                # append new state to q table
                self.Q = self.Q.append(pd.Series([0]*len(self.actions), index=self.Q.columns, name=state))
            if next_state not in self.Q.index:
                # append new state to q table
                self.Q = self.Q.append(pd.Series([0]*len(self.actions), index=self.Q.columns, name=next_state))
            if not done:
                next_Q_values = self.Q.loc[next_state, :]
                next_Q_value = np.max(next_Q_values)
                target_Q = reward + self.gamma*(next_Q_value)
            else:
                target_Q = reward
            self.Q.loc[state, action] +=  self.rate*(target_Q - self.Q.loc[state, action])
    
    def save(self):
        self.Q.to_csv("Q_table.csv")

    def load(self):
        try:
            read_csv = pd.read_csv("Q_table.csv", index_col=0)
            self.Q = read_csv
            print("Q table has been updated")
        except:
            print("there is no previous Q-table")

    def copy_from(self, other):
        self.Q = other.Q
        



