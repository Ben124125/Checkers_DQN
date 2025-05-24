from DQN import DQN
from DQN_Agent import DQN_Agent
from Random_Agent import Random_Agent
from Checkerss import Checkerss
from ReplayBuffer import ReplayBuffer
from State import State
from Graphics import Graphics
import wandb
import torch 

epochs = 50000

C = 200
batch = 64
learning_rate = 0.00001
path = "Data\_Adam_DQN_PARAM_50K_White_f3.pth"

def main ():
    env = Checkerss()
    player1 = DQN_Agent(player=-1, env=env, train=True)
    player2 = Random_Agent(player=-1, env=env)
    replay = ReplayBuffer()
    Q = player1.DQN
    Q_hat :DQN = Q.copy()
    Q_hat.train = False
    optim = torch.optim.Adam(Q.parameters(), lr=learning_rate)
    scores = []
    avgLoss = 0
    avgLosses = []
    score = [0,0,0]   
    losses = []
    loss_count = 0
    score_1000 = [0,0,0]
     ################# Wandb.init #####################
    
    #checkpoint21: 128, 258, 512, 128, 64 death-=3 gamma 0.99 LR = 0.00001 Schedule: 5000, 10000, 15000 death -3 c = 3 decay = 20000
    wandb.init(
        # set the wandb project where this run will be logged
        project="Checkers",
        resume=False, 
        id='Checkers 50k White f3',
        # track hyperparameters and run metadata
        config={
        "name": "Checkers 1",
        "checkpoint": path,
        "learning_rate": learning_rate,
        "architecture": "FNN 128, 258, 512, 128, 64, 4",
        "Schedule": "5000, 10000, 15000 gamma=0.99",
        "epochs": epochs,
        "start_epoch": 1,
        "decay": 5000,
        "gamma": 0.99,
        "batch_size": batch, 
        "C": C
            }
        )
    
    #################################
    for epoch in range(1,epochs + 1):
        next_state = None
        state = env.set_init_state()
        done = False
        step = 1
        action = player2.get_action(state=state)
        state_1 = env.next_state(state,action, player_Train = -1)
        state = state_1[0]
        while not done:
            step += 1
            action = player1.get_action(state=state, epoch=epoch, train=True)
            
            after_state, reward1 = env.next_state(state, action, player_Train = -1)
            reward1 = reward1 * -1
            done, win = env.end_of_game(state=after_state)
            if done or step > 200:
                if win == 0:
                    win = env.winSum(state=state)
                replay.push(state, action, reward1, after_state, done)
                break
            after_action = player2.get_action(state=after_state, epoch=epoch)
           
            next_state, reward2 = env.next_state(after_state, after_action, player_Train = -1)
            reward2 = reward2 * -1
            done, win = env.end_of_game(state=after_state)
            reward = reward1 + reward2
            if done or step > 200:
                if win == 0:
                    win = env.winSum(state=state)
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

            if loss_count <= 1000:
                avgLoss = (avgLoss * loss_count + loss.item()) / (loss_count + 1)
                loss_count += 1
            else:
                avgLoss += (loss.item()-avgLoss)* 0.00001 
        print(f'epoch: {epoch}',  end="\r")

        if win == 1:
            score[0] += 1
        elif win == -1:
            score[1] += 1
        else:
            score[2] += 1

        if epoch % C == 0:
            Q_hat.load_state_dict(Q.state_dict())
       
        if (epoch  ) % 100 == 0:
            print(f'epoch: {epoch} loss: {loss.item()} score: {score}')
            print('avgLoss: ', avgLoss)
            scores.append(score)
            losses.append(loss.item())
            avgLosses.append(avgLoss)
            poch = 0
            wandb.log ({
                "score": score[1],
                "loss": loss.item(),
                "avg_loss": avgLoss
                })
            score = [0,0,0] 
    print('scores: ', scores) 
    print('losses: ', losses)  
    print('avgLosses: ', avgLosses)
    player1.save_param(path)

if __name__ == '__main__':
    main()