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

# epochs = 1000
# batch_size = 64
gamma = 0.99 
MSELoss = nn.MSELoss()

class DQN_Agent:
    def __init__(self,env : Checkerss, player = 1, parametes_path = None, train = True) -> None:
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train(train)

        # self.train = train
        self.player = player
        self.env = env
        # self.FROM = ()
        # self.To = ()

    def train (self, train):
          self.train = train
          if train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_action (self,state: State, epoch = 0, events= None, train = False):
        # print('state player DQN agent is: ', state.player)
        if state.blocked:
            # state.legal_actions = ((-1, -1), (-1, -1))
            return [(-1, -1), (-1, -1)]
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actions = state.legal_actions
        #print('all state legal actions: ', self.env.alllegalActions(state))  
        # print('state DQN legal action: ', state.legal_actions)
        # action_tensor = torch.tensor(actions).reshape(-1, 4)
        # print(action_tensor)
        # action_tensor2 = torch.tensor(actions).reshape(-1)
        # print(action_tensor2)
        actions_np = np.array(actions)
        # print(actions_np)
        actions_lst = actions_np.tolist()
        # print(actions_lst)
        if actions_lst == []:
            # print('player is: ', self.player)
            # time.sleep(2)
            return [-2,-2, -2,-2]
        if train and rnd < epsilon:
            if state.Isblocked:
                selected_piece= random.choice(state.block_come_from)
            else:
                selected_piece =  random.choice(actions)
            return selected_piece
        
        state_tensor = state.toTensor()
        # action_np = np.array(actions)
        # action_tensor = torch.from_numpy(action_np)
        action_tensor = torch.tensor(actions).reshape(-1, 4)
        expand_state_tensor = state_tensor[0].unsqueeze(0).repeat((len(action_tensor),1))
        # state_action = torch.cat((expand_state_tensor, action_tensor ), dim=1)
        
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
        # print('q values are: ', Q_values) 
        max_index = torch.argmax(Q_values)
        # max_idxLst = max_index.tolist()
        # self.env.legal(state, actions[max_idxLst][0] , actions[max_idxLst][1])
        # print('the max action is: ', actions[max_index])
        
        if actions == []:
            # print('player is: ', self.player)
            # time.sleep(2)
            return [(-2,-2), (-2,-2)]
        
        # print('max action is: ',actions[max_index])
        return actions[max_index]
       




#############################################################################################
    def get_actions (self, states, dones):
        actions = []
        boards_tensor = states[0]
        actions_tensor = states[1]
        for i, state in enumerate(boards_tensor):
            if dones[i].item():
                # actions_np = np.array((-1,-1,-1,-1))
                actions.append([-2,-2,-2,-2])
            else:
                actions.append(self.get_action(State.tensorToState(boards_tensor[i], actions_tensor[i],player = self.player), train=True)) #SARSA = True / Q-learning = False
        actions_tensor = torch.tensor(actions).reshape(-1, 4)
        #  # actions_tensor = torch.tensor(actions).reshape(-1, 4)
        # # print()
        # # actions_np = np.array(actions).reshape(128,2)
        # # print(actions_np)
        # actions_tensor = torch.tensor(actions)
        # # actions_tensor = torch.from_numpy(actions_np)
        # return actions_tensor
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