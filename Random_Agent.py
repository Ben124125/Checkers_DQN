import random
from Checkerss import Checkerss
from State import State
from Graphics import *
import pygame
import time

class Random_Agent:
    def __init__(self, player, env : Checkerss, graphics: Graphics = None):
        self.player = player
        self.env = env
        self.graphics = graphics

    def get_action(self, events = None, epoch = None, state = None, train = None) : 
        if state.blocked:
            return [(-1, -1), (-1, -1)]
        
        all_moves = self.env.alllegalActions(state)
       
        if len(all_moves) != 0:
            selected_piece = random.choice(all_moves)
            return [selected_piece[0], selected_piece[1]]
        
        if self.env.avmoves == []:
           return [(-2,-2), (-2,-2)] 
        return None 