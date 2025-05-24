from State import State
from Graphics import *
from collections import defaultdict
import numpy as np

class Checkerss:
    def __init__(self, state = None):
        self.state = state # move to state
        self.eat_moves = None  # avmoves if must eat
        self.avmoves= [] # avmoves 
        self.winner = 0
       

    def move (self, action):
        if action == [(-1, -1), (-1, -1)]:
            self.state.Isblocked = False
            self.state.blocked = False
            
            self.state.switch_players()
            self.state.legal_actions = self.get_all_legal_Actions(self.state)
            print('player turn blocked: ', self.state.player)
            print('legal moves: ', self.state.legal_actions)
            self.state.blocked_next = True
            return   
           
        if action == [(-2,-2), (-2,-2)]:
            isEnd, win =  self.end_of_game(self.state)
            self.state = win
            return   isEnd
        
        From, To = action
        rowf,colf = From
        rowt, colt = To
             
        row = (From[0] + To[0]) // 2
        col = (From[1] + To[1]) // 2
        
        if self.state.block_come_from != [] and  self.state.Isblocked:
            if (self.state.block_come_from != []):
                for i in range(len(self.state.block_come_from)):
                    if (To in self.state.block_come_from[i]):
                        self.state.board[row, col] = 0
                        break
         
                
        if rowf - (self.check_number_sign(self.state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt):
            self.state.board[row, col] = 0     
        elif rowf + (self.check_number_sign(self.state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt):
            self.state.board[row, col] = 0     
        if self.state.board[From] == 2 or self.state.board[From] == -2:
            moves = self.moveking(self.state,From)[0]
            for move in moves:
                r, c = move
                if rowt == r and colt == c and self.state.board[move] == 0: # problem
                    self.eatAllInRow(self.state, From, To)
        self.state.board[From], self.state.board[To] = self.state.board[To], self.state.board[From] 

      
        if rowt == 0 and self.state.player == 1:
            self.state.board[To] = 2
        elif rowt == 7 and self.state.player == -1:
            self.state.board[To] = -2     

        if self.state.block_come_from != []:
            self.state.block_must_go_to = action[1]

        if self.state.Isblocked and not self.state.blocked_next and self.state.board[self.state.block_must_go_to] != 0 and self.check_number_sign(self.state.board[self.state.block_must_go_to]) == self.check_number_sign(self.state.player):
            self.state.blocked = True
        
        if self.state.Isblocked and [action[0], action[1]] not in self.state.block_come_from:
                self.state.blocked = False
                self.state.Isblocked = False
                self.state.block_come_from = []
                self.state.block_must_go_to = []


        self.state.switch_players()
        print('player turn: ', self.state.player)    
        self.state.legal_actions = self.get_all_legal_Actions(self.state)
        print('legal moves: ', self.state.legal_actions)
        

    def switch_players (self, state):
        if state.player == 1:     
            self.state.player = -1
        else:
            self.state.player = 1

 
    def legal(self,  state: State, From, To):
        if To[0] >  8 and To[0] < -1 or state.board[To] != 0: # check if in board and to empty
            return False
        rowf,colf = From
        rowt, colt = To
        row = (From[0] + To[0]) // 2
        col = (From[1] + To[1]) // 2 
        self.state = state

        if ((state.board[From] == 2 and state.player == 1) or (state.board[From] == -2 and state.player == -1)) and (self.must_eat(state) == False or self.must_eat_king(state)):
            moves = self.moveking(state,From)[0]
            if state.block_must_go_to != [] and state.block_come_from != [] and not state.Isblocked and state.block_must_go_to != From:
                return False
            for move in moves: # each tuple represent the place the player is going to
                r, c = move
                if rowt == r and colt == c and state.board[move] == 0 and self.Is_piece_king_eat(state,From) and self.must_eat_king(state):
                    if self.double_eat(state=state,From=From,To=To):
                        return True
                    return True
                elif rowt == r and colt == c and state.board[move] == 0 and  self.must_eat(state) == False and self.must_eat_king(state) == False:
                    return True

        elif rowf - self.check_number_sign(state.player) == rowt and (colf - 1 == colt or colf + 1 == colt) and self.must_eat(state) == False and self.must_eat_king(state) == False and From != state.block_must_go_to: # basic movement
            return True
        
        #  check if mid isn't empty and mid does not have same color
        elif self.check_number_sign(state.board[row, col]) != self.check_number_sign(state.player) and state.board[row, col] != 0: # eat
            if state.block_must_go_to != [] and  state.block_come_from != [] and not state.Isblocked and state.block_must_go_to != From:
                return False  
            
            if rowf - (self.check_number_sign(state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt) and self.must_eat(state): 
                self.double_eat(state=state,From=From,To=To)
                return True
            if rowf + (self.check_number_sign(state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt): # checks double eat
                if self.double_eat(state=state,From=From,To=To):
                    return True

            if state.block_must_go_to != [] and rowf + (self.check_number_sign(state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt):
                self.double_eat(state=state,From=From,To=To)
                return True
        else:
            return False

    def double_eat(self,state,From, To):
        if abs(state.board[From]) == 2:
            if To not in self.moveking(state,From)[0]:
                return False
            
            stateee = state.copy()
            self.eatAllInRow(stateee, From, To)
            stateee.board[To] = stateee.board[From]
            stateee.board[From] = 0
            if self.Is_piece_king_eat(state=stateee,From=To):
                if [From,To] not in state.block_come_from:
                    state.block_come_from.append([From,To])
                state.block_must_go_to = To
                state.Isblocked = True   

        elif abs(state.board[From]) == 1:
            stateee = state.copy()
            row = (From[0] + To[0]) // 2
            col = (From[1] + To[1]) // 2
            stateee.board[row,col] = 0
            stateee.board[To] = stateee.board[From]    
            stateee.board[From] = 0
            if self.must_eat(state = stateee, Is_Double_eat=To):
                if [From,To] not in state.block_come_from:
                    state.block_come_from.append([From,To])
                state.block_must_go_to = To
                state.Isblocked = True   

        return state.Isblocked
    

    def next_state (self, state: State, action, player_Train):
        next_state = state.copy()
        if action == [(-1, -1), (-1, -1)]:
            next_state.Isblocked = False
            next_state.blocked = False
            next_state.switch_players()
            next_state.legal_actions = self.get_all_legal_Actions(next_state)
            next_state.blocked_next = True
            return  next_state, 0 
        if action == [-2,-2, -2,-2]:
            self.end_of_game(next_state)
           
            if next_state.end_of_game == 0:
                reward = 0
                # if next_state.player == player_Train * -1:
                #     reward = next_state.eat_num * 0.05  # cuz white eats black after switching players
                # else:
                #     #  reward = next_state.eat_num   * -0.5
                #     reward = next_state.eat_num * -0.01
                # next_state.eat = 0 
            else:
                reward = next_state.end_of_game
            return next_state, reward     

        From, To = action
        rowf,colf = From
        rowt, colt = To
             
        row = (From[0] + To[0]) // 2
        col = (From[1] + To[1]) // 2
        if next_state.block_come_from != [] and next_state.Isblocked:
            if (next_state.block_come_from != []):
                for i in range(len(next_state.block_come_from)):
                    if (To == next_state.block_come_from[i]):
                        next_state.board[row, col] = 0
                        break
        if rowf - (self.check_number_sign(next_state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt): # eat, deleting the player who gonna be eaten
            next_state.board[row, col] = 0  
            next_state.eat_num = 1 
        elif rowf + (self.check_number_sign(next_state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt):
            next_state.board[row, col] = 0     
            next_state.eat_num = 1 
        if next_state.board[From] == 2 or next_state.board[From] == -2:
            moves = self.moveking(next_state,From)[0]
            for move in moves:
                r, c = move
                if rowt == r and colt == c and next_state.board[move] == 0:
                    self.eatAllInRow(next_state, From, To)

        if rowt == 0 and next_state.player == 1:
            next_state.board[To] = 2
        elif rowt == 7 and next_state.player == -1:
            next_state.board[To] = -2     
        else:
            next_state.board[action[1]] = next_state.board[From] # moves the eating player
        next_state.board[action[0]] = 0                # moves the eating player 
        

        if next_state.block_come_from != []:
            next_state.block_must_go_to = action[1]


        if next_state.Isblocked and not next_state.blocked_next and next_state.board[next_state.block_must_go_to] != 0 and self.check_number_sign(next_state.board[next_state.block_must_go_to]) == self.check_number_sign(next_state.player):
            next_state.blocked = True

        if next_state.Isblocked and [action[0], action[1]] not in next_state.block_come_from:
            next_state.blocked = False
            next_state.Isblocked = False
            next_state.block_come_from = []
            next_state.block_must_go_to = []



        next_state.switch_players()

        self.end_of_game(next_state)
        if next_state.end_of_game == 0:
            reward = 0
            # if next_state.eat_num != 0:
            #     if next_state.player == player_Train * -1: # has to be state
            #         reward = next_state.eat_num * 0.05   # cuz white eats black after switching players
            #     else:
            #         #  reward = next_state.eat_num   * -0.5
            #         reward = next_state.eat_num   * -0.01
            #     next_state.eat = 0 
        else:
            reward = next_state.end_of_game
        next_state.legal_actions = self.get_all_legal_Actions(next_state)
        # print('reward is: ', reward)
        return next_state, reward    
        

    def eatAllInRow(self,state,From, To):
        board = state.board

        rowf, colf = From
        rowt, colt = To
        eat_reward =  0
        if rowf < rowt and colf < colt: #d 4
            while rowf + 1< rowt and colf +1 < colt:
                if board[rowf +1, colf +1] != 0:
                    eat_reward +=1
                board[rowf+1, colf+1] = 0
                rowf += 1
                colf += 1
        elif rowf < rowt and colf > colt: # d3
            while rowf +1 <rowt and colf -1 > colt:
                if board[rowf +1, colf -1] != 0:
                    eat_reward +=1
                board[rowf+1, colf-1] = 0 
                rowf += 1
                colf -= 1      
        elif rowf > rowt and colf < colt: #d2
            while rowf -1 >rowt and colf +1 < colt:
                if board[rowf -1, colf +1] != 0:
                    eat_reward +=1
                board[rowf-1, colf+1] = 0 
                rowf -= 1
                colf += 1  
        elif rowf > rowt and colf > colt: # d1
            while rowf -1 >rowt and colf -1 > colt:
                if board[rowf -1, colf -1] != 0:
                    eat_reward +=1
                board[rowf-1, colf-1] = 0  
                rowf -= 1
                colf -= 1                             
        state.eat_num = eat_reward
        return state
                    
    def check_number_sign(self,number):
        if number >0: 
            return 1
        elif number < 0:
            return -1
        return 0            
    
    def moveking(self,state : State, From):
        board = state.board
        r, c = From
        rowf, colf = From
        moves = []
        eat_moves = []
        king_eat1 = False
        king_eat2 = False
        king_eat3 = False
        king_eat4 = False
        Is_king_must_eat = False
        
        while (rowf < 6 and colf <= 7 and rowf >= 0 and  colf > 1):
            rowf += 1;colf -= 1
            if (colf >0 and rowf < 7 and self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat1) and board[rowf+1, colf-1] == 0):
                Is_king_must_eat = True
                king_eat1 = True
                eat_moves.append((rowf+1,colf-1))
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                    moves.append((rowf,colf))   
            else:
                colf = 100

        rowf, colf = r, c    
        while (rowf < 6 and colf <= 6 and rowf >= 0 and  colf >= 0):
            rowf += 1;colf += 1
            if (colf < 7 and rowf < 7 and self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat2) and board[rowf+1, colf+1] == 0):
                Is_king_must_eat = True
                king_eat2 = True
                eat_moves.append((rowf+1,colf+1))
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                    moves.append((rowf,colf))   
            else:
               colf = 100

        rowf, colf = r, c    
        while (rowf <= 7 and colf <= 7 and rowf >= 1 and  colf > 1):
            rowf -= 1;colf -= 1
            if (colf >0 and rowf > 0 and self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat3)and board[rowf-1, colf-1] == 0):
                Is_king_must_eat = True
                king_eat3 = True
                eat_moves.append((rowf-1,colf-1))   
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                    moves.append((rowf,colf))   
            else:
                colf = 100

        rowf, colf = r, c    
        while (rowf <= 7 and colf <= 6 and rowf >= 1 and  colf >= 0):
            rowf -= 1;colf += 1
            if (colf < 7 and rowf > 0 and self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat4) and board[rowf-1, colf+1] == 0):
                Is_king_must_eat = True
                king_eat4 = True
                eat_moves.append((rowf-1,colf+1))  
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                    moves.append((rowf,colf))   
            else:
                colf = 100

        if eat_moves != []:
            self.eat_moves = eat_moves
            return eat_moves, Is_king_must_eat

        return moves,  Is_king_must_eat           
        

    def winSum(self, state: State):
        if state.board.sum() > 0:
            return 1
        elif state.board.sum() < 0:
            return -1
        else: 
            return 0
    def end_of_game (self, state: State): # fix end of game
        countWhite, countBlack = 0, 0
        if state.legal_actions == [] and (self.find_identical_black_2d(state) != [] and self.find_identical_white_2d(state) != []):
            return True, 0
        elif state.legal_actions == [] and (self.find_identical_black_2d(state) == []): # build a function that takes all > 0
            return True, -1
        elif  state.legal_actions == [] and self.find_identical_white_2d(state) == []:
             return True, 1

        white_remaining, black_remaining = False, False
        board = state.board
        for row in range(ROWS):
            for col in range(COLS):
                if board[row, col] > 0:
                    black_remaining = True
                    countBlack +=1
                    self.winner = 1
                elif board[row, col] < 0:
                    white_remaining = True
                    countWhite +=1
                    self.winner = -1
                    
        if white_remaining and black_remaining:
                return False, 0
        state.end_of_game = self.winner
        return True, self.winner

    def Is_piece_king_eat(self,state:State, From):
        isMustEat = self.moveking(state, From)[1]
        return isMustEat

    def must_eat_king(self,state:State):
        isMustEat = False
        for row in range(ROWS):
                for col in range(COLS):
                    if state.player == 1:
                        if state.board[row, col] == 2:
                            isMustEat = self.moveking(state, (row,col))[1]
                            if isMustEat:
                                break
                    elif state.player == -1:
                        if state.board[row, col] == -2:
                            isMustEat = self.moveking(state, (row,col))[1]
                            if isMustEat:
                                break
                if isMustEat:
                    break   
        return isMustEat              
    def must_eat(self, state: State, Is_Double_eat = None):
        board = state.board
        isMustEat = False
        if state.player >0:
           
            for row in range(ROWS):
                for col in range(COLS):
                    if Is_Double_eat != None:
                        if board[row,col] > 0 and row < 6 and col < 6 and (board[row+1,col+1] < 0  and board[row+2,col+2] == 0 and ((row,col) == Is_Double_eat )):
                            isMustEat = True
                            break          
                        elif board[row,col] > 0 and row < 6 and col > 1 and (board[row+1, col-1] < 0 and board[row+2, col-2] == 0 and ((row,col) == Is_Double_eat)):    
                            isMustEat = True
                            break   
                    if board[row,col] > 0  and row != 0 and col != 0 and col != 7 and col != 6 and col != 1  and row != 1 and (Is_Double_eat == None or (row,col) == Is_Double_eat): # maybe adding row != 6 and row != 7
                        if  ((board[row-1,col+1] < 0  and board[row-2,col+2] == 0 ) or ( board[row-1, col-1] < 0 and board[row-2, col-2] == 0) ) :
                            isMustEat = True
                            break
                    elif board[row,col] > 0 and col >= 6 and row > 1 and (Is_Double_eat == None or (row,col) == Is_Double_eat):    
                        if (board[row-1,col-1] < 0  and board[row-2,col-2] == 0):
                            isMustEat = True
                            break
                    elif board[row,col] > 0 and col <= 1 and row > 1 and (Is_Double_eat == None or (row,col) == Is_Double_eat):
                        if (board[row-1,col+1] < 0  and board[row-2,col+2] == 0):
                            isMustEat = True
                            break
                    else:
                        isMustEat = False
                    if isMustEat == True:
                        break 
                if isMustEat == True:
                    break               
        elif state.player <0:
            for row in range(ROWS):
                for col in range(COLS):
                    if Is_Double_eat != None:
                        if board[row,col] < 0 and row > 1 and col < 6 and (board[row-1,col+1] > 0  and board[row-2,col+2] == 0 and ((row,col) == Is_Double_eat)):
                            isMustEat = True
                            break          
                        elif board[row,col] < 0 and row > 1 and col > 1 and (board[row-1, col-1] > 0 and board[row-2, col-2] == 0 and ((row,col) == Is_Double_eat)):    
                            isMustEat = True
                            break     
                    if board[row,col] < 0 and row != 7  and col != 0 and col != 7  and col != 6 and col != 1 and row != 6 and (Is_Double_eat == None or (row,col) == Is_Double_eat):
                        if ((board[row+1,col+1] > 0  and board[row+2,col+2] == 0 ) or ( board[row+1, col-1] > 0 and board[row+2, col-2] == 0)):    
                            isMustEat = True
                            break
                    elif board[row,col] < 0 and col >= 6 and row < 6 and (Is_Double_eat == None or (row,col) == Is_Double_eat):    
                        if (board[row+1,col-1] > 0  and board[row+2,col-2] == 0):
                            isMustEat = True
                            break
                    elif board[row,col] < 0 and col <= 1 and col < 6 and row < 6 and (Is_Double_eat == None or (row,col) == Is_Double_eat):
                        if (board[row+1,col+1] > 0  and board[row+2,col+2] == 0):
                            isMustEat = True
                            break  
                    else:
                        isMustEat = False                
                    if isMustEat == True:
                        break   
                if isMustEat == True:       
                    break           
        return isMustEat                                     


    def remove_duplicate(self,lst):
        seen = set()
        un_lst = []
        for inner_list in lst:
            tuple_inner_list = tuple(inner_list)
            if tuple_inner_list not in seen:
              un_lst.append(inner_list)
              seen.add(tuple_inner_list)
        return un_lst

    def get_all_legal_Actions(self, state):
        moves = self.find_identical_indices_2d(state)
        avmoves = []
        king_double_eat_avmoves = []
        double_eat_avmoves = []
        self.avmoves = []
        if state.blocked :
            avmoves.append([(-1,-1),(-1,-1)])
     
        elif state.player > 0:
                if  state.blocked_next:
                    state.block_come_from = [] 
                    state.block_must_go_to = [] 
                    state.blocked_next = False
                blackMoves = self.find_identical_black_2d(state)
                for i in range(len(blackMoves)):
                    for j in range(len(moves)):
                        From = (blackMoves[i])
                        To = (moves[j])
                        if self.legal(state, From, To) and state.block_must_go_to != [] and state.Isblocked and (state.block_must_go_to == From or  [From,To] in state.block_come_from) and state.board[From] < 2 and To not in avmoves:
                            avmoves.append([From,To])   
                            double_eat_avmoves.append([From,To])   
                        elif self.legal(state, From, To) and state.block_must_go_to != []  and (state.block_must_go_to == From) and state.board[From] < 2 and To not in avmoves:
                            avmoves.append([From,To])   
                            double_eat_avmoves.append([From,To])     
                        elif self.legal(state, From, To) and To not in avmoves:
                            if state.board[From] == 2 and [From,To] not in avmoves:
                                avmoves.append([From,To])
                            elif state.block_come_from == [] and state.block_must_go_to == []  and [From,To] not in avmoves:
                                avmoves.append([From,To])
                        if self.eat_moves != None and state.block_must_go_to == From and state.board[From] == 2: # king double eat moves
                            for o in range(len(self.eat_moves)):
                                if [From,self.eat_moves[o]] not in king_double_eat_avmoves: 
                                  king_double_eat_avmoves.append([From,self.eat_moves[o]])
                    self.eat_moves = None       
                 
                       
        elif state.player < 0:
                if   state.blocked_next:
                    state.block_come_from = [] 
                    state.block_must_go_to = [] 
                    state.blocked_next = False
                whiteMoves = self.find_identical_white_2d(state)
                for i in range(len(whiteMoves)):
                    for j in range(len(moves)):
                        From = (whiteMoves[i])
                        To = (moves[j])
                        if self.legal(state, From, To) and state.block_must_go_to != [] and state.Isblocked and (state.block_must_go_to == From or  [From,To] in state.block_come_from) and state.board[From] > -2  and To not in avmoves:
                            avmoves.append([From,To]) 
                            double_eat_avmoves.append([From,To])   
                        elif self.legal(state, From, To) and state.block_must_go_to != [] and (state.block_must_go_to == From ) and state.board[From] > -2  and To not in avmoves:
                            avmoves.append([From,To]) 
                            double_eat_avmoves.append([From,To])      
                        elif self.legal(state, From, To) and To not in avmoves:
                            if state.board[From] == -2 and [From,To] not in avmoves:
                                avmoves.append([From,To])
                            elif state.block_come_from == [] and state.block_must_go_to == [] and [From,To] not in avmoves:
                                avmoves.append([From,To]) 
                        if self.eat_moves != None and state.block_must_go_to == From :
                            for o in range(len(self.eat_moves)):
                                if [From,self.eat_moves[o]] not in king_double_eat_avmoves and state.board[From] == -2: 
                                    king_double_eat_avmoves.append([From,self.eat_moves[o]])  
                        
                    self.eat_moves = None                
                   

        if king_double_eat_avmoves != []:
            avmoves = king_double_eat_avmoves
        elif double_eat_avmoves != [] and (2 * self.check_number_sign(state.player) not in state.board):
            avmoves = double_eat_avmoves
        self.avmoves = avmoves     
        state.legal_actions = avmoves
        return self.avmoves

    def alllegalActions(self, state):
        return state.legal_actions


    # return all empty places
    def find_identical_indices_2d(self, state):
        board = state.board
        moves = []
        for row in range(len(board)):
            for col in range(len(board[row])):
              if board[row][col] == 0:
                moves.append((row, col))
        return moves
    
    # retuen all black places
    def find_identical_black_2d(self, state):
        board = state.board
        moves = []
      
        for row in range(len(board)):
            for col in range(len(board[row])):
            #   if board[row][col] > 1 and board[row][col] != 0:
            #     print('asd')
              if board[row][col] > 0:
                moves.append((row, col))
        return moves
    
    # return all white places
    def find_identical_white_2d(self, state):
        board = state.board
        moves = []
        
        for row in range(len(board)):
            for col in range(len(board[row])):
            #   if board[row][col] < -1 and board[row][col] != 0:
            #      print('tyij')
              if board[row][col] < 0:
                moves.append((row, col))
        return moves
    
    def set_init_state (self):
        self.state = State()
        self.state.legal_actions = self.get_all_legal_Actions(self.state)
        return self.state

   
