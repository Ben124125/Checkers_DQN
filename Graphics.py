import pygame
# from Checkerss import Checkerss
# from Human_Agent import Human_Agent
# from State import State

# #WIDTH, HEIGHT = 800, 800

# ROWS, COLS = 8,8
# SQUARE_SIZE = 100
# LINE_WIDTH = 20
# FPS = 60

# # H_WIDHT, H_HEIGHT = 300, 100
# # M_WIDHT, M_HEIGHT = 300, 300




# SANDY_WOOD = (205,133,63)
# BURTY_WOOD = (222,184,135)
# PERU_WOOD = (205,133,63)
# # DARK_WOOD = (139,69,19)
# BlACK = (0,0,0)
# GREEN = (0,255,0)
# WHITE =(255,255,255)
# LIGHTRED = (255, 30, 60)
# RED = (75,0,0)

#------------------------------------------


WIDTH, HEIGHT = 800, 900


H_WIDTH, H_HEIGHT = 800, 100
M_WIDTH, M_HEIGHT = 800, 800


ROWS, COLS = 8,8
SQUARE_SIZE = 100
LINE_WIDTH = 60
FPS = 60

SANDY_WOOD = (205,133,63)
BURTY_WOOD = (222,184,135)
PERU_WOOD = (205,133,63)
# DARK_WOOD = (139,69,19)
BlACK = (0,0,0)
GREEN = (0,255,0)
WHITE =(255,255,255)
LIGHTRED = (255, 30, 60)
RED = (75,0,0)


# RED = (255, 0, 0)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# BLUE = (0, 0, 255)
LIGHTGRAY = (211,211,211)
# GREEN = (0, 128, 0)
# CADETBLUE1 = (152,245,255)


class Graphics:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.header_surf = pygame.Surface((H_WIDTH, H_HEIGHT))
        self.main_surf = pygame.Surface((M_WIDTH, M_HEIGHT))
        pygame.display.set_caption('Checkers')
        self.board = {}
        # self.env = env
        # self.human = human
        self.selected_piece = None
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0

    def draw(self, state):

        
        # self.draw_header(state)
        self.main_surf.fill(BlACK)
        # self.screen.fill(BlACK)
        
        for row in range(ROWS):
            for col in range(row % 2, ROWS,2):
                pygame.draw.rect(self.main_surf,SANDY_WOOD, (row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

        self.load_img()
        self.draw_pieces(state)


        self.screen.blit(self.header_surf, (0,0))
        self.screen.blit(self.main_surf, (0, 100))  # Position header at the top
        #self.screen.blit(self.main_surf, (0, H_HEIGHT))  # Position main area below the header
        #pygame.draw.line(self.header_surf, RED, (1 * SQUARE_SIZE, 0), (1 * SQUARE_SIZE, HEIGHT), width= LINE_WIDTH)
        
        pygame.display.update()
        
    def draw_header(self, state = None,env = None,action = None):
        self.header_surf.fill(LIGHTGRAY)
        
        if state.player > 0:
          self.write('                                  turn is: Black' )
          if env.must_eat(state) or env.must_eat_king(state):  
            self.write_below(' black u must eat white')
        #   elif action != None and not env.legal(state,action[0], action[1]):
        #     self.write_below('gud action')    
        #   else:
        #       self.write_below('illegel action')  
        elif state.player < 0:
          self.write('                                  turn is: White' )  
          if env.must_eat(state) or env.must_eat_king(state):  
            self.write_below(' white u must eat black')  
        #   elif action != None and not env.legal(state,action[0], action[1]):
        #     self.write_below('gud action')  
        #   else:
        #       self.write_below('illegel action')   

    def write (self, txt):
        font = pygame.font.SysFont('Modern', 48)
        txt_surf = font.render(txt, True, BlACK)
        self.header_surf.blit(txt_surf, (10,10))

    def write_below(self, txt):
        font = pygame.font.SysFont('Modern', 30)
        txt_surf = font.render(txt, True, BlACK)
        self.header_surf.blit(txt_surf, (20,45))

    def write_below_below(self, txt):
        font = pygame.font.SysFont('Modern', 30)
        txt_surf = font.render(txt, True, BlACK)
        self.header_surf.blit(txt_surf, (20,70))    

    def load_img(self):
        black_piece_img = pygame.image.load('img/black_piece_chess.png')
        black_king_img = pygame.image.load('img/black_king.png')
        white_piece_img = pygame.image.load('img/white_piece_chess.png')
        white_king_img = pygame.image.load('img/white_king.png')
        self.black_piece_img = pygame.transform.scale(black_piece_img,(80, 80))
        self.white_piece_img = pygame.transform.scale(white_piece_img,(80, 80))

        self.black_king_img = pygame.transform.scale(black_king_img,(80, 80))
        self.white_king_img = pygame.transform.scale(white_king_img,(80, 80))

    def draw_pieces(self, state):
        board = state.board
        for row in range(ROWS):
            for col in range(COLS):
                if board[row,col] != 0:
                    self.draw_piece((row,col), board[row, col], state)

    def draw_piece(self, row_col, player, state):
        if player > 0:
            img = self.black_piece_img
            if state.board[row_col] == 2:
                img = self.black_king_img
        elif player < 0:
            img = self.white_piece_img
            if state.board[row_col] == -2:
                img = self.white_king_img
        else:
            img = None
            
        x, y = self.calc_pos(row_col)
        self.main_surf.blit(img,(x + 10,y + 10)) 

    def draw_valid_moves(self, moves):
        for move in moves: # dictionary keys
            row, col = move
            pygame.draw.circle(self.screen, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
        pygame.display.update()

    def calc_pos(self, row_col):
        row,col = row_col
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        return x, y
    
    def calc_row_pos(self,pos):
        x,y = pos
        if y<100:
            return None
        row = abs(y-HEIGHT)  // SQUARE_SIZE
        col = x // SQUARE_SIZE

        return row,col
    def calc_row_pos_first(self,pos):
        x,y = pos
        row = (y - 112) //100
        col = x //100
        return row,col

    def __call__(self,state):
        self.draw(state)