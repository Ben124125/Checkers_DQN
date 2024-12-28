from typing import Any
from Checkerss import Checkerss
import pygame

from Graphics import *

class Human_Agent:

    def __init__(self, player, env : Checkerss, graphics: Graphics):
        self.player = player
        self.env = env
        self.graphics = graphics
        self.mode = 1 # 1-pick from; 2-pick TO
        self.FROM = ()
        self.To = ()
        self.count =1
        self.countnum = 0
        
    def get_action (self, events, state = None):
        
        if state.blocked:
            print("legal moves blocked: ", self.env.alllegalActions(state))
            return ((-1, -1), (-1, -1))
         

        if  self.countnum == 0:
                #print("av av av av moves: ", self.env.alllegalActions(state))
                # print("available moves: ", self.env.alllegalActions(state))
                self.countnum = 1
                if self.env.avmoves == []:
                    return ((-2,-2),(-2,-2))   
        for event in events:
            # if event.type == pygame.MOUSEMOTION and self.countnum == 0:
            #     #print("av av av av moves: ", self.env.alllegalActions(state))
            #     print("available moves: ", self.env.alllegalActions(state))
            #     self.countnum = 1
            #     if self.env.avmoves == []:
            #         return ((-2,-2),(-2,-2))     
            # if event.type == pygame.MOUSEMOTION:
            #     if self.env.avmoves == []:
            #         return ((-2,-2),(-2,-2))     
            #-------------------------------------------------------------------------    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print('--------------------------------------')
                pos = event.pos
                # print('pos: ', pos)
                row_col = self.graphics.calc_row_pos_first(pos)
                # self.env.alllegalActions(state)
                # self.countnum = 0
                # print('state player human agent is: ', state.player)
                # print('state legal actions: ', self.env.alllegalActions(state))  
                if self.mode == 1:
                    print("legal moves: ", self.env.alllegalActions(state))
                    if (state.board[row_col]  > 0 and self.player > 0) or (state.board[row_col]<0 and self.player <0):
                        self.FROM = row_col
                        self.mode = 2
                    # print(f'you choose: {row_col}')
                    # print('value in from: ', state.board[row_col])
                    return None

                if self.mode == 2:
                    print('state player human agent is: ', state.player)
                    # print('state legal actions: ', self.env.alllegalActions(state))  
                    # print('state legal actions: ', self.env.alllegalActions(state))  
                    # print("available moves: ", )  
                    if self.env.avmoves == []:
                        return ((-2,-2),(-2,-2)) 
                    # state.moves += 1        
                    if self.env.legal(state, self.FROM, row_col):
                        self.mode = 1
                        print(f'action {self.FROM} -> {row_col} ')
                        self.countnum = 0
                        self.To = row_col
                        return self.FROM, row_col    
                    else:
                        # print(f'Illegal actiom {self.FROM} -> {row_col}')
                        self.graphics.write_below_below(' illegal action')
                        self.mode = 1
                        self.countnum = 0
        return None

    def __call__(self, events=None, state=None):
        return self.get_action(events, state)