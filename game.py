from typing import Any
import pygame
from Graphics import *
from Checkerss import Checkerss
from State import State
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent
# from MinMax_Agent import MinMax_Agent
# from AlphaBeta_Agent import AlphaBeta_Agent
# from DDQN_Agent import DDQN_Agent
import time

pygame.init()
clock = pygame.time.Clock()
graphics = Graphics()

env = Checkerss()
env.set_init_state()


# player1 = Random_Agent(1, env, graphics)
# player2 = Random_Agent(-1, env, graphics)

# player1 = Human_Agent(player=1, env=env, graphics=graphics)


player2 = Human_Agent(player=-1, env=env, graphics=graphics)

player1 = DQN_Agent(player=1, env=env)
print('<----------------------------------------------------------------------------------------------------------------->>>>>>>>')

# player2 =  DQN_Agent(player=-1, env=env)


graphics.draw_header(env.state, env)
FPS = 60


def main():
    run = True
    step_b = 1
    step_w = 1
    player = player1
    while(run):    
        pygame.event.pump()   
        events = pygame.event.get()
        for event in events:
            pygame.event.pump()   
            if event.type == pygame.QUIT:
                run = False
        pygame.event.pump()     
        
        action = player.get_action(events=events, state=env.state)
        
        if action:
            print('<------------------------------------------------------------------------------------------------------------------->')
            env.move(action)
            player = switch_players(player)
            # print(Random_Agent(env))
            graphics.draw_header(env.state, env, action)
            end_of_game = env.end_of_game(env.state, player.player)
            # if env.avmoves == []:
            #     winner = winner * -1   
            #     end_of_game = True, winner
            if player.player == 1:
                #  print(f'step b: {step_b}', end="\r")
                 step_b += 1
            elif player.player == -1:
                #  print(f'step w: {step_w}', end="\r")
                 step_w += 1
            if end_of_game[0] is not False:
                graphics.draw(env.state)
                if end_of_game[1] == 1:
                    print("Black has won!")
                elif end_of_game[1] == -1:
                    print("White has won!")
                else:
                    print("Draw")    
                # time.sleep(3)
                run = False
                print(f'step b: {step_b}')
                print(f'step w: {step_w}')
                ######### reset: init state + player = 1
            # time.sleep(0.3)
        graphics(env.state)
          
        pygame.display.update()
        clock.tick(FPS)

    pygame.time.wait(20)

def switch_players(player):
    if player == player1:
        return player2
    else:
        return player1


if __name__ == '__main__':
    main()    







# from typing import Any
# import pygame
# from Graphics import *
# from Checkerss import Checkerss
# from State import State
# from Human_Agent import Human_Agent
# from Random_Agent import Random_Agent
# # from MinMax_Agent import MinMax_Agent
# # from AlphaBeta_Agent import AlphaBeta_Agent
# # from DDQN_Agent import DDQN_Agent
# import time

# pygame.init()
# clock = pygame.time.Clock()
# graphics = Graphics()
# env = Checkerss(State())


# # player1 = Random_Agent(1, env, graphics)
# # player2 = Random_Agent(-1, env, graphics)

# # player1 = Human_Agent(1, env, graphics)
# # player2 = Human_Agent(-1, env, graphics)

# player1 = None
# player2 = None


# graphics.draw_header(env.state, env)
# FPS = 60


# def start_screen():
#     pygame.init()
#     win = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption('Select Agent Types')
    
#     # Colors
#     colors = {'button': (200, 200, 200), 'highlight': (150, 150, 150), 'text': (0, 0, 0)}

#     # Default selections
#     player1_agent = 'Random'
#     player2_agent = 'Random'

#     font = pygame.font.SysFont(None, 48)
#     clock = pygame.time.Clock()

#     while True:
#         win.fill(LIGHTGRAY)

#         # Draw buttons and text
#         pygame.draw.rect(win, colors['button'], (100, 200, 200, 40))
#         pygame.draw.rect(win, colors['button'], (500, 200, 200, 40))
#         pygame.draw.rect(win, colors['button'], (100, 300, 200, 40))
#         pygame.draw.rect(win, colors['button'], (500, 300, 200, 40))
#         pygame.draw.rect(win, colors['button'], (300, 500, 200, 40))

#         # Render text
#         text1 = font.render(f'Player 1: {player1_agent}', True, colors['text'])
#         text2 = font.render(f'Player 2: {player2_agent}', True, colors['text'])
#         text_play = font.render('Play', True, colors['text'])
#         win.blit(text1, (50, 100))
#         win.blit(text2, (450, 100))
#         win.blit(text_play, (350, 510))

#         pygame.display.flip()
        
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 return None, None
           
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 print('pos is: ',pos)
#                 # Check if the play button is clicked
#                 if 300 < pos[0] < 500 and 500 < pos[1] < 540:
#                     pygame.quit()
#                     return player1_agent, player2_agent
#                 # Check if player 1 agent is selected
#                 if 100 < pos[0] < 300 and 200 < pos[1] < 240:
#                     player1_agent = 'Human'
#                 if 500 < pos[0] < 700 and 200 < pos[1] < 240:
#                     player2_agent = 'Human'
#                 # Check if player 2 agent is selected
#                 if 100 < pos[0] < 300 and 300 < pos[1] < 340:
#                     player1_agent = 'Random'
#                 if 500 < pos[0] < 700 and 300 < pos[1] < 340:
#                     player2_agent = 'Random'
#         return player1_agent, player2_agent


# def main(p1 = None,p2 = None):
#     run = True

#     if p1 == 'Human':
#         player1 = Human_Agent(1,env,graphics)
#     else:
#         player1 = Random_Agent(1,env,graphics)
        
#     if p2 == 'Human':
#        player2 = Human_Agent(-1, env, graphics)
#     else:
#         player2 = Random_Agent(-1, env, graphics)

#     player = player1
#     while(run):    
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 run = False
                
#         action = player.get_action(events=events, state=env.state)
        
#         if action:
#             env.move(action)
#             player = switch_players(player)
#             # print(Random_Agent(env))
#             graphics.draw_header(env.state, env, action)
#             end_of_game = env.end_of_game(env.state, player.player)
#             # if env.avmoves == []:
#             #     winner = winner * -1   
#             #     end_of_game = True, winner
           
#             if end_of_game != False:
#                 graphics.draw(env.state)
#                 if end_of_game[1] == 1:
#                     print("Black has won!")
#                 elif end_of_game[1] == -1:
#                     print("White has won!")
#                 else:
#                     print("Draw")    
#                 #time.sleep(3)
#                 run = False
#             #time.sleep(0.3)
#         graphics(env.state)
          
#         pygame.display.update()
#         clock.tick(FPS)

#     pygame.time.wait(20)

# def switch_players(player):
#     if player == player1:
#         return player2
#     else:
#         return player1


# if __name__ == '__main__':
#     print("drtdr")
#     p1, p2 = start_screen()
#     print(f"p1: {0}, p2 {1}", p1,p2)
#     if p1 and p2:
#         main(p1,p2)    






