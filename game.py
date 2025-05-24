from typing import Any
import pygame
from Graphics import *
from Checkerss import Checkerss
from State import State
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent
import time


def start_screen():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Select Agent Types')
    
    # Colors
    colors = {'button': (255, 255, 255), 'highlight': (150, 150, 150), 'text': (0, 0, 0)}

    # Default selections
    player1_agent = 'Random'
    player2_agent = 'Random'

    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    while True:
        win.fill(SANDY_WOOD)

        # Draw buttons and text
        pygame.draw.rect(win, colors['button'], (100, 200, 200, 40)) # human
        human1 = font.render('Human', True, colors['text'])
        win.blit(human1, (150, 205)) # position text
        pygame.draw.rect(win, colors['button'], (500, 200, 200, 40)) # human
        human2 = font.render('Human', True, colors['text'])
        win.blit(human2, (550, 205)) # position text


        pygame.draw.rect(win, colors['button'], (100, 300, 200, 40)) # random
        random1 = font.render('Random', True, colors['text'])
        win.blit(random1, (145, 305)) # position text
        pygame.draw.rect(win, colors['button'], (500, 300, 200, 40)) # random
        random2 = font.render('Random', True, colors['text'])
        win.blit(random2, (545, 305)) # position text

        pygame.draw.rect(win, colors['button'], (100, 400, 200, 40)) # ai
        AI1 = font.render('AI', True, colors['text'])
        win.blit(AI1, (180, 405)) # position text
        pygame.draw.rect(win, colors['button'], (500, 400, 200, 40)) # ai
        AI2 = font.render('AI', True, colors['text'])
        win.blit(AI2, (580, 405)) # position text

        pygame.draw.rect(win, colors['button'], (300, 500, 200, 40)) # submit

        # Render text
        text1 = font.render(f'Black P1: {player1_agent}', True, colors['text'])
        text2 = font.render(f'White P2: {player2_agent}', True, colors['text'])
        text_play = font.render('Play', True, colors['text'])
        win.blit(text1, (50, 100))
        win.blit(text2, (450, 100))
        win.blit(text_play, (365, 505))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print('pos is: ',pos)
                # Check if the play button is clicked
                if 300 < pos[0] < 500 and 500 < pos[1] < 540:
                    # pygame.quit()
                    return player1_agent, player2_agent
                # Check if player 1 agent is selected
                if 100 < pos[0] < 300 and 200 < pos[1] < 240:
                    player1_agent = 'Human'
                if 500 < pos[0] < 700 and 200 < pos[1] < 240:
                    player2_agent = 'Human'
                # Check if player 2 agent is selected
                if 100 < pos[0] < 300 and 300 < pos[1] < 340:
                    player1_agent = 'Random'
                if 500 < pos[0] < 700 and 300 < pos[1] < 340:
                    player2_agent = 'Random'

                if 100 < pos[0] < 300 and 400 < pos[1] < 440:
                    player1_agent = 'AI'
                if 500 < pos[0] < 700 and 400 < pos[1] < 440:
                    player2_agent = 'AI'

        # return player1_agent, player2_agent
def end_screen(winner = None):
    pygame.init()
    end_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers ')
    
    # Colors
    colors = {'button': (255, 255, 255), 'highlight': (150, 150, 150), 'text': (0, 0, 0)}

    # Default selections

    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    run = True
    while run:
        end_screen.fill(SANDY_WOOD)
        pygame.draw.rect(end_screen, colors['button'], (300, 500, 200, 40)) # submit
        pygame.draw.rect(end_screen, colors['button'], (300, 600, 200, 40))
        # Render text
        text1 = font.render(f'Winner: {winner}', True, colors['text'])
        text_quit = font.render('Quit', True, colors['text'])
        text_play = font.render('Play Again', True, colors['text'])
        end_screen.blit(text1, (50, 100))

        end_screen.blit(text_play, (325, 505))
        end_screen.blit(text_quit, (365, 605))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                return None, None
           
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print('pos is: ',pos)
                # Check if the play button is clicked
                if 300 < pos[0] < 500 and 500 < pos[1] < 540:
                    # pygame.quit()
                    pygame.init()
                    
                    global graphics
                    graphics = Graphics()

                    global env
                    env = Checkerss()
                    env.set_init_state()

                    graphics.draw_header(env.state, env)
                    FPS = 60

                    print("drtdr")
                    p1, p2 = start_screen()
                    print(f"p1: {0}, p2 {1}", p1,p2)
                    run = False
                    if p1 and p2:
                        main(p1,p2)    
                elif  300 < pos[0] < 500 and 600 < pos[1] < 640:
                    pygame.quit()
                    run = False

def main(p1 = None,p2 = None):
    run = True
    step_b = 1
    step_w = 1
    global player1
    global player2
    if p1 == 'Human':
        player1 = Human_Agent(1,env,graphics)
    elif p1 == "AI":
        path= "Data\_Adam_DQN_PARAM_50K_Black_f3.pth"
        player1 = DQN_Agent(player=1, env=env,parametes_path=path, train=False)
    else:
        player1 = Random_Agent(1,env,graphics)
        
    if p2 == 'Human':
       player2 = Human_Agent(-1, env, graphics)
    elif p2 == "AI":
        path2 = "Data\_Adam_DQN_PARAM_50K_White_f3.pth"
        player2 = DQN_Agent(player=-1, env=env,parametes_path=path2, train=False) 
    else:
        player2 = Random_Agent(-1, env, graphics)

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
            graphics.draw_header(env.state, env)
            end_of_game = env.end_of_game(env.state)
            if player.player == 1:
                 step_b += 1
            elif player.player == -1:
                 step_w += 1
            if end_of_game[0] is not False:
                graphics.draw(env.state)
                if end_of_game[1] == 1:
                    print("Black has won!")
                    time.sleep(3)
                    end_screen('black')
                    break
                elif end_of_game[1] == -1:
                    print("White has won!")
                    time.sleep(3)
                    end_screen('white')
                    break
                else:
                    print("Draw")  
                    time.sleep(6)
                    end_screen('draw') 
                    break 
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
    pygame.init()
    clock = pygame.time.Clock()
    graphics = Graphics()

    env = Checkerss()
    env.set_init_state()

    player1 = None
    player2 = None
    graphics.draw_header(env.state, env)
    FPS = 60

    print("drtdr")
    p1, p2 = start_screen()
    print(f"p1: {0}, p2 {1}", p1,p2)
    if p1 and p2:
        main(p1,p2)  





