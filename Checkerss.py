from State import State
from Graphics import *
from collections import defaultdict
import numpy as np

class Checkerss:
    def __init__(self, state = None):
        self.state = state # move to state
        self.From_king = None
        self.avmoves_king = []   
        self.avmoves= []
        self.winner = 0
        self.must_eating = 0

    def move (self, action):
        if action == [(-1, -1), (-1, -1)]:
            # self.switch_players(self.state)
            self.state.Isblocked = False
            self.state.blocked = False
            self.state.switch_players()
            self.state.legal_actions = self.get_all_legal_Actions(self.state)
            print('player turn blocked: ', self.state.player)
            print('legal moves: ', self.state.legal_actions)
           
            self.must_eating = 1
            return   
        
             
        if action == ((-2,-2), (-2,-2)):
            isEnd, win =  self.end_of_game(self.state,self.state.player)
            self.state = win
            return   isEnd
        
        From, To = action
        rowf,colf = From
        rowt, colt = To
             
        row = (From[0] + To[0]) // 2
        col = (From[1] + To[1]) // 2

        if self.state.block_come_from != [] and not self.state.Isblocked:
            if (self.state.block_come_from != []):
                for i in range(len(self.state.block_come_from)):
                    if (To == self.state.block_come_from[i]):
                        self.state.board[row, col] = 0
                        self.state.blocked_next = 1
                        self.state.block_come_from = [] 
                        break
            # else:
            #     for i in range(len(self.state.block_must_go_to[1])):
            #         if (To == self.state.block_must_go_to[i]):
            #             self.state.board[row, col] = 0
            #             self.state.block_must_go_to = []
            #             break
                # print('true true black can eat twice')
               
                
        if rowf - (self.check_number_sign(self.state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt):
            self.state.board[row, col] = 0     
            self.state.eat = False

        if self.state.board[From] == 2 or self.state.board[From] == -2:
            moves = self.moveking(self.state,From)[0]
            # print('moves are: ', moves)
            for move in moves:
                r, c = move
                if rowt == r and colt == c and self.state.board[move] <= 0: # problem
                    self.eatAllInRow(self.state, From, To)
        self.state.board[From], self.state.board[To] = self.state.board[To], self.state.board[From] 

      
        if rowt == 0 and self.state.player == 1:
            self.state.board[To] = 2
        elif rowt == 7 and self.state.player == -1:
            self.state.board[To] = -2     

        # if self.state.blocked:
        #     self.state.switch_players()
        #     self.state.legal_actions = self.get_all_legal_Actions(self.state)
        
        # self.switch_players(self.state) # delete
        # if self.state.blocked:
        #     print('blocked: ',self.state.player)
        
        # block = False
        # if self.state.blocked:
        #     block = True
        # print('o')
        # o = 1
          # if not self.state.blocked:
        #     self.state.switch_players()
        #     self.state.legal_actions = self.get_all_legal_Actions(self.state)
        # if not self.state.blocked:
        #     self.state.switch_players()
        #     self.state.legal_actions = self.get_all_legal_Actions(self.state)
        # else:
            
        #     self.state.legal_actions = self.get_all_legal_Actions(self.state)
        #     self.state.switch_players()

        # block = False
        # if self.state.blocked and self.state.blocked_next == 1:
        #     self.state.blocked_next = 0
        #     block = True
        # self.state.blocked = block
        if self.state.Isblocked:
            self.state.blocked = True
            
        # if action != ((-1, -1), (-1, -1)):    
        self.state.switch_players()
        print('player turn: ', self.state.player)    
        self.state.legal_actions = self.get_all_legal_Actions(self.state)
        print('legal moves: ', self.state.legal_actions)
        # self.state.Isblocked = False
        # block = False
        # if self.state.blocked and self.state.blocked_next == 1:
        #     self.state.blocked_next = 0
        #     block = True
        # self.state.blocked = block
        
        # self.get_all_legal_Actions(self.state)

        # if self.state.moves == 1:
        #     self.state.switch_players()
        #     self.state.legal_actions = self.get_all_legal_Actions(self.state)
        # else:
        #     self.state.legal_actions = self.get_all_legal_Actions(self.state)
        #     self.state.switch_players()
       
      
        # self.state.switch_players()
        

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
       
        # if state.board[From] == 2 or state.board[From] == -2:
        #     moves = self.moveking(state,From)
        #     # print('moves are: ', moves)
        #     for move in moves:
        #         r, c = move
        #         if rowt == r and colt == c and state.board[move] <= 0:
        #             return True

        if ((state.board[From] == 2 and state.player == 1) or (state.board[From] == -2 and state.player == -1)) and (self.must_eat(state) == False or self.must_eat_king(state)):
            moves = self.moveking(state,From)[0]
            # print('moves are: ', moves)
            for move in moves: # each tuple represent the place the player is going to
                r, c = move
                if rowt == r and colt == c and state.board[move] == 0 and self.Is_piece_king_eat(state,From) and self.must_eat_king(state):
                    return True
                elif rowt == r and colt == c and state.board[move] == 0 and  self.must_eat(state) == False and self.must_eat_king(state) == False:
                    return True

       
        elif rowf - self.check_number_sign(state.player) == rowt and (colf - 1 == colt or colf + 1 == colt) and self.must_eat(state) == False and self.must_eat_king(state) == False: # basic movement
            # print("move succefully")
            
            return True
        
        #  check if mid isn't empty and mid does not have same color
        elif self.check_number_sign(state.board[row, col]) != self.check_number_sign(state.player) and state.board[row, col] != 0: # eat
            state.eat = 1
            if state.block_must_go_to != [] and state.block_come_from == [] and state.block_must_go_to != From:
                return False  
            
            if rowf - (self.check_number_sign(state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt): #checks if double eat (+-2, +-2)
                # print("must eat: ", self.must_eat(state))
                if  rowt > 1 and rowt < 6 and state.block_come_from != (rowt,colt): # changed 2 ifs below start colt > 1 and colt < 6 from this main row
                    # if (colt > 1 and (state.board[rowt - self.check_number_sign(self.state.player), colt - 1] != self.check_number_sign(self.state.player) or state.board[rowt - self.check_number_sign(self.state.player), colt + 1] != self.check_number_sign(self.state.player)) and (state.board[rowt - (self.check_number_sign(self.state.player) *2), colt-2] ==0 or state.board[rowt - (self.check_number_sign(self.state.player) *2), colt+2] ==0)): # maybe deleting the 6
                    if (colt > 1 and [From,To] not in state.block_come_from and state.board[rowt - self.check_number_sign(state.player), colt - 1] != self.check_number_sign(state.player) and state.board[rowt - self.check_number_sign(state.player), colt - 1] != 0 and state.board[rowt-(self.check_number_sign(state.player) *2), colt-2] ==0):  
                        state.block_come_from.append([(rowf, colf),(rowt, colt)])
                        # self.state.block_come_from.append()
                        state.block_must_go_to = To
                        # self.state.block_must_go_to.append((rowt, colt))
                        # self.state.block_must_go_to.append([(rowt  - (self.check_number_sign(state.player) *2), colt-2)])
                        # if colt + 2 < 8 and state.board[(rowt  - (self.check_number_sign(state.player) *2), colt+2)] == 0:
                        #   self.state.block_must_go_to[1].append((rowt  - (self.check_number_sign(state.player) *2), colt+2))
                        # # if self.state.blocked_next == 1: 
                        # #     self.state.blocked = True
                        state.Isblocked = True
                    elif (colt < 6 and [From,To] not in state.block_come_from and state.board[rowt - self.check_number_sign(state.player), colt + 1] != self.check_number_sign(state.player) and state.board[rowt - self.check_number_sign(state.player), colt + 1] != 0 and state.board[rowt - (self.check_number_sign(state.player) *2), colt+2] ==0):
                        state.block_come_from.append([(rowf, colf),(rowt, colt)])
                        #self.state.block_come_from.append()
                        state.block_must_go_to = To
                        #self.state.block_must_go_to.append((rowt, colt))
                        # # self.state.block_must_go_to = rowt  - (self.check_number_sign(self.state.player) *2), colt+2
                        # self.state.block_must_go_to.append([(rowt  - (self.check_number_sign(state.player) *2), colt+2)])
                        # if colt-2 > 0 and state.board[(rowt  - (self.check_number_sign(state.player) *2), colt-2)] == 0:
                        #     self.state.block_must_go_to[1].append((rowt  - (self.check_number_sign(state.player) *2), colt-2))
                        
                        # if self.state.blocked_next == 1:  
                        #     self.state.blocked = True
                        state.Isblocked = True
                return True
        # elif state.board[From] == 2 or state.board[From] == -2:
        #     moves = self.moveking(state,From)
        #     # print('moves are: ', moves)
        #     for move in moves:
        #         r, c = move
        #         if rowt == r and colt == c and state.board[move] <= 0:
        #             return True
        else:
            return False

    
    def next_state (self, state: State, action):
        next_state = state.copy()
        if action == [(-1, -1), (-1, -1)]:
            next_state.Isblocked = False
            next_state.blocked = False
            next_state.switch_players()
            next_state.legal_actions = self.get_all_legal_Actions(next_state)
            
            self.must_eating = 1
            return  next_state, 0 
        if action == [-2,-2, -2,-2]:
            self.end_of_game(next_state,player=next_state.player)
           
            if next_state.end_of_game == 0:
                reward = 0
                if next_state.player == -1:
                    reward = next_state.eat_num * 5  # cuz white eats black after switching players
                else:
                    #  reward = next_state.eat_num   * -0.5
                    reward = next_state.eat_num * -2
                next_state.eat = 0 
            else:
                reward = next_state.end_of_game * 100
            return next_state, reward     
        # if action == ((-2,-2), (-2,-2)):
        #     return self.end_of_game(self.state,self.state.player)
        
        # next_state.board[action[0]] = 0
        # next_state.board[action[1]] = state.player
        From, To = action
        rowf,colf = From
        rowt, colt = To
             
        row = (From[0] + To[0]) // 2
        col = (From[1] + To[1]) // 2
        # print('player turn is: ', next_state.player)
        # print('player legal actions: ', next_state.legal_actions)
        # if next_state.block_come_from != [] and next_state.block_must_go_to != []: # eat twice
        #     if (From[0] == state.block_come_from[0] and From[1] == next_state.block_come_from[1] and To[0] == next_state.block_must_go_to[0] and To[1] == next_state.block_must_go_to[1]):
        #         # print('true true black can eat twice')
        #         next_state.board[row, col] = 0
        #         next_state.block_come_from = [] 
        #         next_state.block_must_go_to = []


        # if next_state.block_come_from != [] or next_state.block_must_go_to != [] and not next_state.Isblocked:
        #     if (next_state.block_come_from != [] and To == next_state.block_come_from[0]):
        #         next_state.board[row, col] = 0
        #         next_state.blocked_next = 1
        #         next_state.block_come_from = [] 
        #     else:
        #         for i in range(len(next_state.block_must_go_to)):
        #             if (To == next_state.block_must_go_to[i]):
        #                 next_state.board[row, col] = 0
        #                 next_state.block_must_go_to = []
        #                 break
        if next_state.block_come_from != [] and not next_state.Isblocked:
            if (next_state.block_come_from != []):
                for i in range(len(next_state.block_come_from)):
                    if (To == next_state.block_come_from[i]):
                        next_state.board[row, col] = 0
                        next_state.blocked_next = 1
                        next_state.block_come_from = [] 
                        break
        if rowf - (self.check_number_sign(next_state.player) *2) == rowt and (colf - 2 == colt or colf + 2 == colt): # eat, deleting the player who gonna be eaten
            next_state.board[row, col] = 0  
            next_state.eat = False  
            next_state.eat_num = 1 

        if next_state.board[From] == 2 or next_state.board[From] == -2:
            moves = self.moveking(next_state,From)[0]
            # print('moves are: ', moves)
            for move in moves:
                r, c = move
                if rowt == r and colt == c and next_state.board[move] <= 0:
                    self.eatAllInRow(next_state, From, To)

        if rowt == 0 and next_state.player == 1:
            next_state.board[To] = 2
        elif rowt == 7 and next_state.player == -1:
            next_state.board[To] = -2     
        else:
            next_state.board[action[1]] = next_state.board[From] # moves the eating player
        next_state.board[action[0]] = 0                # moves the eating player 
        

        if next_state.Isblocked:
            next_state.blocked = True
            
        # if action != ((-1, -1), (-1, -1)):    
        # self.state.switch_players()

        
        # block = False
        # if next_state.blocked:
        #     block = True

        next_state.switch_players()

        self.end_of_game(next_state,player=next_state.player)
        if next_state.end_of_game == 0:
            reward = 0
            if next_state.eat_num != 0:
                if next_state.player == -1:
                    reward = next_state.eat_num * 5   # cuz white eats black after switching players
                else:
                    #  reward = next_state.eat_num   * -0.5
                    reward = next_state.eat_num   * -2
                next_state.eat = 0 
        else:
            reward = next_state.end_of_game * 100
        next_state.legal_actions = self.get_all_legal_Actions(next_state)
        # next_state.blocked = block
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
            # return
        elif rowf < rowt and colf > colt: # d3
            while rowf +1 <rowt and colf -1 > colt:
                if board[rowf +1, colf -1] != 0:
                    eat_reward +=1
                board[rowf+1, colf-1] = 0 
                rowf += 1
                colf -= 1
            # return       
        elif rowf > rowt and colf < colt: #d2
            while rowf -1 >rowt and colf +1 < colt:
                if board[rowf -1, colf +1] != 0:
                    eat_reward +=1
                board[rowf-1, colf+1] = 0 
                rowf -= 1
                colf += 1  
            # return
        elif rowf > rowt and colf > colt: # d1
            while rowf -1 >rowt and colf -1 > colt:
                if board[rowf -1, colf -1] != 0:
                    eat_reward +=1
                board[rowf-1, colf-1] = 0  
                rowf -= 1
                colf -= 1                        
            # return        
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
        lst = [[rowf,colf],[rowf,colf],[rowf,colf],[rowf,colf]]
        moves = []
        eat_moves = []
        # eat_reward =  np.zeros((4))
        # king_must_eat = False
        king_eat1 = False
        king_eat2 = False
        king_eat3 = False
        king_eat4 = False
        Is_king_must_eat = False
        while (rowf < 6 and colf <= 7 and rowf >= 0 and  colf > 1):
            rowf += 1;colf -= 1

             
            if (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat1) and board[rowf+1, colf-1] == 0):
                # if board[rowf, colf] != 0:
                #     eat_reward[0] +=1
                Is_king_must_eat = True
                # king_must_eat = True
                king_eat1 = True
                eat_moves.append((rowf+1,colf-1))
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):

                # if board[rowf, colf] != 0:
                #     eat_reward[0] +=1
                # if king_must_eat:
                #     if board[rowf,colf] == 0:
                #         eat_moves.append((rowf,colf))
                # else:
                    moves.append((rowf,colf))   

            else:
                colf = 100
        rowf, colf = r, c    
        while (rowf < 6 and colf < 6 and rowf >= 0 and  colf >= 0):
            rowf += 1;colf += 1
            if (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat2) and board[rowf+1, colf+1] == 0):
                # if board[rowf, colf] != 0:
                #     eat_reward[1] +=1
                Is_king_must_eat = True
                # king_must_eat = True
                king_eat2 = True
                eat_moves.append((rowf+1,colf+1))
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                # if board[rowf, colf] != 0:
                #     eat_reward[1] +=1
                # if king_must_eat:
                #     if board[rowf,colf] == 0:
                #         eat_moves.append((rowf,colf))
                # else:
                    moves.append((rowf,colf))   

            else:
               colf = 100
        rowf, colf = r, c    
        while (rowf <= 7 and colf <= 7 and rowf > 1 and  colf > 1):
            rowf -= 1;colf -= 1
            if (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat3)and board[rowf-1, colf-1] == 0):
                # if board[rowf, colf] != 0:
                #     eat_reward[2] +=1
                Is_king_must_eat = True
                king_eat3 = True
                # king_must_eat = True    
                eat_moves.append((rowf-1,colf-1))
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                # if board[rowf, colf] != 0:
                #     eat_reward[2] +=1
                # if king_must_eat:
                #     if board[rowf,colf] == 0:
                #         eat_moves.append((rowf,colf))
                # else:
                    moves.append((rowf,colf))   

            else:
                colf = 100
        rowf, colf = r, c    
        while (rowf <= 7 and colf < 6 and rowf > 1 and  colf >= 0):
            rowf -= 1;colf += 1
            if (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player) and (self.check_number_sign(board[rowf,colf]) != 0 or king_eat4) and board[rowf-1, colf+1] == 0):
                # if board[rowf, colf] != 0:
                #     eat_reward[3] +=1
                Is_king_must_eat = True
                king_eat4 = True
                # king_must_eat =True    
                eat_moves.append((rowf-1,colf+1))
            elif (self.check_number_sign(board[rowf,colf]) != self.check_number_sign(state.player)):
                # if board[rowf, colf] != 0:
                #     eat_reward[3] +=1
                # if king_must_eat:
                #     if board[rowf,colf] == 0:
                #         eat_moves.append((rowf,colf))
                # else:
                    moves.append((rowf,colf))   

            else:
                colf = 100


        # print('moves of the white onje kajshfdk: ', moves)
        # self.state.eat_num = np.amax(eat_reward) # have to return it with the step i wanna do

        if eat_moves != []:
            return eat_moves, Is_king_must_eat

        return moves,  Is_king_must_eat           
        

    def winSum(self, state: State):
        if state.board.sum() > 0:
            return 1
        elif state.board.sum() < 0:
            return -1
        else: 
            return 0
    def end_of_game (self, state: State, player): # fix end of game
        winner = 0
        countWhite, countBlack = 0, 0
        #print('aboavi aboavio aboavi moves black: ', self.avmoves)
        if state.legal_actions == [] and (self.find_identical_black_2d(state) != [] and self.find_identical_white_2d(state) != []):
            # self.find_identical_black_2d(state)
            # self.find_identical_white_2d(state)
            return True, 0
        elif state.legal_actions == [] and (self.find_identical_black_2d(state) == []): # build a function that takes all > 0
            # self.winner = self.winner
            # print('true first')
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
                    #print('aboavi aboavio aboavi moves black: ', self.avmoves)
                    # if self.avmoves == []:
                    #    winner = winner * -1   
                    #    return True, winner 
                elif board[row, col] < 0:
                    white_remaining = True
                    countWhite +=1
                    self.winner = -1
                   # print('aboavi aboavio aboavi moves white: ', self.avmoves)
                    # if self.avmoves == []:
                    #     winner = winner * -1   
                    #     return True, winner 

                    
        # if self.alllegalActions(state) == []:
        #     return True,winner * -1
               
        if white_remaining and black_remaining:
                return False, 0
        state.end_of_game = self.winner
        # print('true second')
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
    def must_eat(self, state: State):
        # if abs(state.player) ==2: # maybe returning
        #     isMustEat = self.moveking(state)[1]
        board = state.board
        isMustEat = False
        # player = self.state.player
        # print('player is: ', player)
        if state.player >0:
           
            for row in range(ROWS):
                for col in range(COLS):
                    # if state.board[row, col] == 2:
                    #      isMustEat = self.moveking(state, (row,col))[1]
                    #      if isMustEat:
                    #          break
                    if board[row,col] > 0  and row != 0 and col != 0 and col != 7 and col != 6 and col != 1  and row != 1: # maybe adding row != 6 and row != 7
                        if  ((board[row-1,col+1] < 0  and board[row-2,col+2] == 0 ) or ( board[row-1, col-1] < 0 and board[row-2, col-2] == 0)) :
                            isMustEat = True
                            # print('Black u must eat 1#')
                            break
                        else:
                            isMustEat = False
                    elif board[row,col] > 0 and col >= 6 and row > 1:    
                        if (board[row-1,col-1] < 0  and board[row-2,col-2] == 0):
                            isMustEat = True
                            # print('Black u must eat 2#')
                            break
                        else:
                            isMustEat = False
                   
                    elif board[row,col] > 0 and col <= 1 and row > 1:
                        if (board[row-1,col+1] < 0  and board[row-2,col+2] == 0):
                            isMustEat = True
                            # print('Black u must eat 3#')
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
                    # if state.board[row, col] == -2:
                    #      isMustEat = self.moveking(state, (row,col))[1]
                    #      if isMustEat:
                    #          break
                    if board[row,col] < 0 and row != 7  and col != 0 and col != 7  and col != 6 and col != 1 and row != 6:
                        if ((board[row+1,col+1] > 0  and board[row+2,col+2] == 0 ) or ( board[row+1, col-1] > 0 and board[row+2, col-2] == 0)):    
                            isMustEat = True
                            # print('White u must eat 1#')   
                            break
                        else:
                            isMustEat = False
                    elif board[row,col] < 0 and col >= 6 and row < 6:    
                        if (board[row+1,col-1] > 0  and board[row+2,col-2] == 0):
                            isMustEat = True
                            # print('White u must eat 2#')   
                            break
                        else:
                            isMustEat = False
                    elif board[row,col] < 0 and col <= 1 and col < 6 and row < 6:
                        if (board[row+1,col+1] > 0  and board[row+2,col+2] == 0):
                            isMustEat = True
                            # print('White u must eat 3#')   
                            break  
                        else:
                            isMustEat = False      
                    if isMustEat == True:
                        break   
                if isMustEat == True:
                    self.state.eat = isMustEat          
                    break   
        # self.state.eat = isMustEat             
        return isMustEat                                     

    
    # def remove_duplicate_lists(lst):
    #  seen = set()
    #  unique_list = []
    #  for inner_list in lst:
    #     # Convert the inner list to a tuple to make it hashable
    #     tuple_inner_list = tuple(inner_list)
    #     if tuple_inner_list not in seen:
    #         unique_list.append(inner_list)
    #         seen.add(tuple_inner_list)
    #  return unique_list

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
        #print('avilable moves are: ', moves)
        self.avmoves = []
        if state.Isblocked:
            avmoves.append([(-1,-1),(-1,-1)])
        elif state.player > 0:
            # if state.block_come_from != []:
            #     for i in range(len(state.block_come_from)):
            #         if [state.block_come_from[i]] not in avmoves:
            #             avmoves.append([state.block_come_from[i]])
            #             break
            # # elif state.block_must_go_to != []:
            # #      avmoves  = state.block_must_go_to
            # else:
                blackMoves = self.find_identical_black_2d(state)
                for i in range(len(blackMoves)):
                    for j in range(len(moves)):
                        From = (blackMoves[i])
                        To = (moves[j])
                        if state.block_must_go_to != [] and state.block_must_go_to == From and self.legal(state, From, To) and To not in avmoves:
                            avmoves.append([From,To])     
                        elif self.legal(state, From, To) and To not in avmoves:
                            if [From,To] not in avmoves:
                                avmoves.append([From,To])
                        if self.avmoves_king != []:
                            for o in range(len(self.avmoves_king)):
                                if self.avmoves_king[o] not in avmoves: 
                                  avmoves.append(self.avmoves_king[o])
                        
                            self.avmoves_king = []   
                       
                       

        elif state.player < 0:
            #  if state.block_come_from != []:
            #     for i in range(len(state.block_come_from)):
            #         if [state.block_come_from[i]] not in avmoves:
            #           avmoves.append([state.block_come_from[i]])
                
            # #  elif state.block_must_go_to != []:
            # #      avmoves  = state.block_must_go_to
            #  else:    
                whiteMoves = self.find_identical_white_2d(state)
                for i in range(len(whiteMoves)):
                    for j in range(len(moves)):
                        From = (whiteMoves[i])
                        To = (moves[j])
                        if state.block_must_go_to != [] and state.block_must_go_to == From and self.legal(state, From, To) and To not in avmoves:
                            avmoves.append([From,To])    
                        elif self.legal(state, From, To) and To not in avmoves:
                            if [From,To] not in avmoves:
                                avmoves.append([From,To]) 
                        if self.avmoves_king != []:
                            #i+= 1
                            for o in range(len(self.avmoves_king)):
                                if self.avmoves_king[o] not in avmoves: 
                                    avmoves.append(self.avmoves_king[o])    
                        
                            ###print('ajsdskaijdasdonasklncajkdsfkjafhnweiufhwejfkhewf: ', self.avmoves_king)
                            self.avmoves_king = []                  
        # for rows in range(ROWS):
        #     for cols in range(COLS):
        #         if (board[rows, cols] != 0 and board[rows, cols] != -1 * state.player):
        #           for i in range(len(moves)):
        #              From = (rows, cols)
        #              To = (moves[i])
        #              #print('the to to to is: ', To)
        #              if self.legal(state, From, To) and To not in avmoves:
        #               avmoves.append(To)
        # print("av av av av moves: ", avmoves )
        self.avmoves = avmoves     
        # if state.blocked:
        #     print('blocked')           
        #print('self avmove av av av av av av av av av av: ', self.avmoves)
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

    # def Islegal (self, state: State, From, To):
    #     if state.board[To] == 0: 
    #         rowf,colf = From
    #         rowt, colt = To

    #         if rowf != rowt and colf != colt: 
    #          if state.board[From] > 0:
    #             row = (From[0] + To[0]) // 2
    #             col = (From[1] + To[1]) // 2

    #             if state.board[From] == 2:
    #                 moves = self.moveking(state,From)
    #                 for move in moves:
    #                     self.avmoves_king.append([From, move])
    #                 return False

    #                 # for move in moves:
    #                 #     r, c = move
    #                 #     if rowt == r and colt == c and state.board[move] <= 0:
    #                 #         self.eatAllInRow( From, To)
    #                 #         return True

    #             elif rowf - 1 == rowt and (colf - 1 == colt or colf + 1 == colt) and self.must_eat(state) == False: # basic movement
    #                return True
                
    #             elif self.state.board[row, col] != self.check_number_sign(self.state.player) and self.state.board[row, col] != 0 and (abs(From[0]- To[0]) > 1 or abs(From[1]- To[1]) > 1): # eat
    #                  if self.state.block_come_from != () and self.state.block_must_go_to != ():
    #                      if (From[0] == self.state.block_come_from[0] and From[1] == self.state.block_come_from[1] and To[0] == self.state.block_must_go_to[0] and To[1] == self.state.block_must_go_to[1]):
    #                          #print('true true black can eat twice')
    #                          self.state.block_come_from = () 
    #                          self.state.block_must_go_to = ()
    #                          return True
    #                      else:
    #                          #print('false false black cant eat twice')
    #                          return False
    #                  elif rowf - 2 == rowt and (colf - 2 == colt or colf + 2 == colt):
    #                       #print("must eat: ", self.must_eat(state))
    #                       if  rowt > 1 and rowt < 6 and colt < 6 and colt > 1:
    #                          if (state.board[rowt - 1, colt - 1] < 0 and state.board[rowt-2, colt-2] ==0): # maybe deleting the 6
    #                             self.state.block_come_from = rowt, colt
    #                             self.state.block_must_go_to = rowt-2, colt-2
    #                             self.state.blocked = True
    #                          elif (state.board[rowt - 1, colt + 1] < 0 and state.board[rowt-2, colt+2] ==0):
    #                             self.state.block_come_from = rowt, colt
    #                             self.state.block_must_go_to = rowt-2, colt+2
    #                             self.state.blocked = True
                              
    #                       return True
    #             else:
    #                 #print('black u cant do it')
    #                 self.state.block_come_from = () 
    #                 self.state.block_must_go_to = ()
    #                 return False
    #             #----------------------------------------------------
    #          elif state.board[From] < 0:
    #             row = (From[0] + To[0]) // 2
    #             col = (From[1] + To[1]) // 2

    #             if state.board[From] == -2:
    #                 moves = self.moveking(state,From)
    #                 for move in moves:
    #                     self.avmoves_king.append([From, move])
    #                 return False
    #                 #print('moves are: ', moves)
    #                 # for move in moves:
    #                 #     r, c = move
    #                 #     if rowt == r and colt == c and state.board[move] >= 0:
    #                 #         self.eatAllInRow( From, To)
    #                 #         return True

    #             elif rowf + 1 == rowt and (colf + 1 == colt or colf - 1 == colt) and self.must_eat(state) == False:
    #                return True

    #             elif self.state.board[row, col] != self.check_number_sign(self.state.player) and self.state.board[row, col] != 0 and (abs(From[0]- To[0]) > 1 or abs(From[1]- To[1]) > 1): # eat
                     
    #                  if self.state.block_come_from != () and self.state.block_must_go_to != ():
    #                     if (From[0] == self.state.block_come_from[0] and From[1] == self.state.block_come_from[1] and To[0] == self.state.block_must_go_to[0] and To[1] == self.state.block_must_go_to[1]):
    #                         #print('true true white can eat twice')
    #                         self.state.block_come_from = () 
    #                         self.state.block_must_go_to = ()
    #                         return True
    #                     else:
    #                         #print('false false white cant eat twice')
    #                         return False
    #                  elif rowf + 2 == rowt and (colf + 2 == colt or colf - 2 == colt):
    #                       #print("must eat: ", self.must_eat(state))
    #                       if  rowt > 1 and rowt < 6 and colt < 6 and colt > 1:
    #                         if (state.board[rowt + 1, colt - 1] > 0 and state.board[rowt+2, colt-2] ==0): #and rowt > 1 and rowt < 6: # maybe deleting the 6
    #                              self.state.block_come_from = rowt, colt
    #                              self.state.block_must_go_to = rowt+2, colt-2
    #                              self.state.blocked = True
    #                         elif (state.board[rowt + 1, colt + 1] > 0 and state.board[rowt+2, colt+2] ==0):
    #                              self.state.block_come_from = rowt, colt
    #                              self.state.block_must_go_to = rowt+2, colt+2
    #                              self.state.blocked = True
    #                       return True
    #             else:
    #                 #print('white u cant do it')
    #                 self.state.block_come_from = () 
    #                 self.state.block_must_go_to = ()
    #                 return False
                
                
    #         #else:
    #             #print("i knew it!")  

    #     return False    
    



if __name__ == '__main__':
    board =[[ 0.,  1.,  0.,  1.,  0.,  1.,  0., -1.],
            [ 0.,  0.,  1.,  0.,  1.,  0.,  1.,  0.],
            [ 0.,  0.,  0.,  1.,  0.,  1.,  0., -1.],
            [ 0.,  0.,  0.,  0., -1.,  0., -1.,  0.],
            [ 0., -1.,  0., -1.,  0., -1.,  0., -1.],
            [-1.,  0., -1.,  0., -1.,  0., -1.,  0.],
            [ 0.,  1.,  0., -1.,  0., -1.,  0.,  1.],
            [ 1.,  0.,  1.,  0.,  1.,  0.,  1.,  0.]]
    board = np.array(board, dtype=int)
    state = State(board=board, player=1)
    env = Checkerss(state)
    # print()
    print(env.alllegalActions(state))

