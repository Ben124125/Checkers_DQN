from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Checkerss import Checkerss
from ReplayBuffer import ReplayBuffer
from State import State
from Graphics import Graphics
import torch 

epochs = 1000

C = 300
batch = 64
learning_rate = 0.01
# Min_buffer = 1000
path = "Data\DQN_PARAM_30K.pth"
# graphics = Graphics()

def main ():
    env = Checkerss()
    player1 = DQN_Agent(player=1, env=env, train=True)
    player2 = Random_Agent(player=-1, env=env)
    replay = ReplayBuffer()
    Q = player1.DQN
    Q_hat :DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.SGD(Q.parameters(), lr=learning_rate)
    scores = []
    # avgLoss = 0
    # avgLosses = []
    score = [0,0,0]   
    score_1000 = [0,0,0]
    for epoch in range(1,epochs):
      
        print ('\nepoch: ', epoch)
      
        # score = [0,0,0]   
        state = env.set_init_state()
        done = False
        step = 1
        # action = [(5,0),(4,1)]
        # after_state, reward = env.next_state(state, action)
        # after_action = [(2,3), (3,2)]
        # next_state, reward = env.next_state(after_state, after_action)
        # state = next_state
        
        while not done:
        
            print(f'\t\t\t      step: {step}', end="\r")
            
            step += 1
            # print("\t\n state: \n", state.board)
            action = player1.get_action(state=state, epoch=epoch, train=True)
            after_state, reward = env.next_state(state, action)
            done, win = env.end_of_game(state=after_state, player=player1)
            if done:
                # if step:
                #     win = env.winSum(state=state)
                replay.push(state, action, reward, after_state, done)
                break
            after_action = player2.get_action(state=after_state, epoch=epoch)
            next_state, reward = env.next_state(after_state, after_action)
            done, win = env.end_of_game(state=after_state, player=player1)
            replay.push(state, action, reward, next_state, done)
            state = next_state

            if epoch < batch:
                continue
            states, actions, rewards, next_states, dones = replay.sample(batch)
            Q_values = Q(states[0], actions)
            next_actions = player1.get_actions(next_states, dones)
            with torch.no_grad():
                Q_hat_Values = Q_hat(next_states[0], next_actions)
        
            loss = Q.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()

        # print("\t\n state: \n", state.board)

        if win == 1:
            score[0] += 1
            print("win is black")
        elif win == -1:
            score[1] += 1
            print("win is white")
        else:
            score[2] += 1
            print("draw")
        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())
       
        # print('score: ', score)
        if (epoch  ) % 100 == 0:
            print(f'epoch: {epoch} loss: {loss.item()} score: {score}')
            scores.append(score)
            poch = 0
            score = [0,0,0]


    player1.save_param(path)

if __name__ == '__main__':
    main()