from Graphics import *
import numpy as np
import torch

class State:
    def __init__(self, board = None,legal_actions = [] ,player = 1):
        if board is not None:
            self.board = board
        else:
            self.board = self.init_board()    
        self.player = player
        self.legal_actions = legal_actions
        self.end_of_game = 0  
        self.blocked = False 
        self.block_must_go_to =[]
        self.block_come_from = []
        self.eat = False
        self.win = 0
        self.eat_num = 0 # change the bool
        # self.moves = 0


    
    def toTensor (self, device = torch.device('cpu')):
        board_np = self.board.reshape(-1)
        board_tensor = torch.tensor(board_np, dtype=torch.float32, device=device)
        actions_np = np.array(self.legal_actions)
        actions_tensor = torch.from_numpy(actions_np)
        return board_tensor, actions_tensor
    
    def tensorToState (state_tensor, actions_tensor ,player = 1):
        board = state_tensor.reshape([8,8]).cpu().numpy()
        actions = actions_tensor.reshape([-1,4]).cpu().numpy()
        actions = list(map(list, actions))
        return State(board, actions, player)
    
    def copy (self):
        newBoard = np.copy(self.board)
        return State(board=newBoard, player=self.player)
    def switch_players (self):
        if self.player > 0:
            self.player = -1
        else:
            self.player = 1

    # def score (self):
    #     return self.board.sum()
    def init_board(self):
        board = np.zeros((ROWS,COLS))
        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == ((row+1) % 2):
                    if row <3:
                        board[row,col] = -1
                    elif row > 4:    
                        board[row,col] = 1
        # board[0,5] = -1
        # board[0,7] = -1
        # board[1,4] = -1
        # board[1,6] = -1
        # board[2,5] = -1
        # board[2,7] = -1


        # board[2,1] = 1
        # board[3,4] = 1
        # board[3,0] = 1
        # board[4,3] = 1
        # board[4,7] = 1
        # board[5,6] = 1
        # board[6,5] = 1
        # board[7,2] = 1
        # board[7,4] = 1

        # print(board)                
        return board    
    