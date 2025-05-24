import math
import random
from typing import Any
import torch
import torch.nn as nn
import numpy as np
from DQN import DQN
from State import State
from Checkerss import Checkerss
from Graphics import *
import time

# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 5000


gamma = 0.99 
MSELoss = nn.MSELoss()

class DQN_Agent:
    def __init__(self,env : Checkerss, player = 1, parametes_path = None, train = True) -> None:
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train(train)

        self.player = player
        self.env = env

    def train (self, train):
          self.train = train
          if train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_action (self,state: State, epoch = 0, events= None, train = False):
        if state.blocked:
            return [(-1, -1), (-1, -1)]
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actions = state.legal_actions
    
        actions_np = np.array(actions)

        actions_lst = actions_np.tolist()

        if actions_lst == []:
            return [-2,-2, -2,-2] 
        if train and rnd < epsilon:
            selected_piece =  random.choice(actions)
            return selected_piece
        
        state_tensor = state.toTensor()
        action_tensor = torch.tensor(actions).reshape(-1, 4)
        expand_state_tensor = state_tensor[0].unsqueeze(0).repeat((len(action_tensor),1))
        
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
        max_index = torch.argmax(Q_values)

        
        if actions == []:
            return [(-2,-2), (-2,-2)]
        
        return actions[max_index]
       




#############################################################################################
    def get_actions (self, states, dones):
        actions = []
        boards_tensor = states[0]
        actions_tensor = states[1]
        for i, state in enumerate(boards_tensor):
            if dones[i].item():
                actions.append([-2,-2,-2,-2])
            else:
                actions.append(self.get_action(State.tensorToState(boards_tensor[i], actions_tensor[i],player = self.player), train=True)) #SARSA = True / Q-learning = False
        actions_tensor = torch.tensor(actions).reshape(-1, 4)

        return actions_tensor
    


    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None,train = False, state=None) -> Any:
        return self.get_action(state, train=train)