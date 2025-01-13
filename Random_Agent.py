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
        # self.mode = 1 # 1-pick from; 2-pick TO
        # self.FROM = ()
        # self.count =1
        # self.countnum = 0


    def get_action(self, events = None, epoch = None, state = None, train = None) : 

        if state.blocked:
            # state.legal_actions = ((-1, -1), (-1, -1))
            return [(-1, -1), (-1, -1)]
        
       
        # print("state player is oasdjapodj: ", state.player)
        all_moves = self.env.alllegalActions(state)
       
        # print("available moves: ", self.env.alllegalActions(state))  
        if len(all_moves) != 0:
           
        #    all_moves = self.env.alllegalActions(self.env.state)
            # if state.block_come_from != []:
            #     selected_piece = state.block_come_from
            # elif state.block_must_go_to != []:
            #     if len(state.block_must_go_to[1]) > 1:
            #         selected_piece = state.block_must_go_to
            #         selected_piece[1] = random.choice(state.block_must_go_to[1])
            #     else:
            #         selected_piece = state.block_must_go_to
            # else:
            if state.Isblocked:
                selected_piece= random.choice(state.block_come_from)
            else:
                selected_piece = random.choice(all_moves)
            
            # print('selected piece: ', selected_piece)
        # for i in range(len(all_moves)):
        #     if all_moves[i][0] == selected_piece:
        #         selected_move = random.choice(all_moves[selected_piece])
        #         print('selected move: ', selected_move)
        #         return (selected_piece,selected_move,all_moves[selected_piece][selected_move])  
            # print('all moves of the moves are: ', all_moves)
            # print(f'selected action {selected_piece[0]} -> {selected_piece[1]}')
            # print('player is: ', self.player)
            
            return selected_piece[0], selected_piece[1]
            # if self.env.legal(state, selected_piece[0], selected_piece[1]):
            #   print(f'selected action {selected_piece[0]} -> {selected_piece[1]}')
            #   print('player is: ', self.player)
            #   return selected_piece[0], selected_piece[1]
            # else:
            #     print(f'illegel action {selected_piece[0]} -> {selected_piece[1]}')
        if self.env.avmoves == []:
            # print('player is: ', self.player)
            # time.sleep(10)
            return [-2,-2, -2,-2]
        return None
        # while all_moves != []:
        #      selected_piece = random.choice(all_moves)
        #selected_move = random.choice(all_moves[selected_piece])
        # print('selected move: ', selected_move)
        #return (selected_piece,selected_move,all_moves[selected_piece][selected_move])  


    # def get_action(self, events = None, state = None, epoch = None): # returns action: ((start_row, start_col), (dest_row, dest_col), [skipped pieces - tuples of row and col])
    #     all_moves = self.get_all_valid_moves(self.player, state) # Dictionary: key - (piece_row, piece_col), value - dictionary: key - (dest_row, dest_col), value - [(skipped_row, skipped_col), ...]
    #     if not all_moves:
    #         print(state)
    #     selected_piece = random.choice(list(all_moves.keys()))
    #     while all_moves[selected_piece] == {}:
    #         selected_piece = random.choice(list(all_moves.keys()))
    #     selected_move = random.choice(list(all_moves[selected_piece].keys()))
    #     return (selected_piece, selected_move, all_moves[selected_piece][selected_move])

    # def get_all_valid_moves(self, player, state):
    #     moves = {}
    #     for row in range(ROWS):
    #         for col in range(COLS):
    #             if (player == -1 and state.board[row][col] < 0) or (player == 1 and state.board[row][col] > 0):
    #                 moves[(row, col)] = self.env.get_valid_moves(state, (row, col))
    #     return moves