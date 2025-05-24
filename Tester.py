from Random_Agent import Random_Agent
# from Fix_Agent import Fix_Agent
from Checkerss import Checkerss
from DQN_Agent import DQN_Agent

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2
        

    def test (self, games_num):
        env = self.env
        player1_win = 0
        player2_win = 0
        draw = 0 
        games = 0
        
        while games < games_num:
            state = env.state
            player = self.player1
            step = 0
            end = env.end_of_game(state)
            while end[0] == False:
                action = player.get_action(state=state, train = False)
                state,_ = env.next_state(state,action, player_Train = 0)
                player = self.switchPlayers(player)
                step += 1
                end = env.end_of_game(state)
                
            if env.end_of_game(state):
                score = end[1]
                if score > 0:
                    player1_win += 1
                elif score < 0:
                    player2_win += 1
                else:
                    end = env.end_of_game(state)
                    draw += 1
                state = env.set_init_state()
                games += 1
                player = self.player1
                print(games, end="\r")
        return player1_win, player2_win, draw        

    def switchPlayers(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def __call__(self, games_num):
        return self.test(games_num)

if __name__ == '__main__':
    # path = 'Data\_Adam_DQN_PARAM_50K_Black_LR2.pth'
    path= "Data\_Adam_DQN_PARAM_50K_Black_f3.pth"
    path2 = "Data\_Adam_DQN_PARAM_50K_White_f3.pth"
    
    print('----------------------------------------------------------')
    for i in range(5): # test white
        env = Checkerss()
        env.set_init_state()
        player1 = Random_Agent(env=env, player=1)
        player2 = DQN_Agent(env=env, player=-1,parametes_path =path2, train=False)
        test = Tester(env,player1, player2)
        print(test.test(100))

    for i in range(5):  # test black
        env = Checkerss()
        env.set_init_state()    
        player1 = DQN_Agent(env=env, player=1,parametes_path=path, train=False)
        player2 = Random_Agent(env=env, player=-1)
        test = Tester(env,player1, player2)
        print(test.test(100))
