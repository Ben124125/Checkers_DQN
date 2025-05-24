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
        self.countnum = 0
        
    def get_action (self, events, state = None):
        
        if state.blocked:
            return [(-1, -1), (-1, -1)]
         

        if  self.countnum == 0:
                self.countnum = 1
                if self.env.avmoves == []:
                    return [(-2,-2), (-2,-2)] 
        for event in events:
            #-------------------------------------------------------------------------    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row_col = self.graphics.calc_row_pos_first(pos)
                if self.mode == 1:
                    if (state.board[row_col]  > 0 and self.player > 0) or (state.board[row_col]<0 and self.player <0):
                        self.FROM = row_col
                        self.mode = 2
                    return None

                if self.mode == 2:
                    if self.env.avmoves == []:
                        return [(-2,-2),(-2,-2)] 
                    if self.env.legal(state, self.FROM, row_col):
                        self.mode = 1
                        print(f'action {self.FROM} -> {row_col} ')
                        self.countnum = 0
                        self.To = row_col
                        return [self.FROM, row_col]
                    else:
                        self.graphics.write_below_below(' illegal action')
                        self.mode = 1
                        self.countnum = 0
        return None

    def __call__(self, events=None, state=None):
        return self.get_action(events, state)