import random
import gym
from gym import spaces


class MinesweeperEnv(gym.Env):
    def __init__(self, game):
        self.game = game

        # required
        self.action_space = spaces.Discrete(self.game.rows * self.game.cols)
        # self.action_space = spaces.Box(low=0, high=1, shape=(self.game.rows, self.game.cols), dtype=int)
        self.observation_space = spaces.Box(low=0, high=10, shape=(self.game.rows, self.game.cols), dtype=int)

        # not required


    def step(self, action):
        i = random.randrange(0, self.game.rows)
        j = random.randrange(0, self.game.cols)
        
        self.game.reveal(i, j)
        state = self.game.known_grid

        reward = 0
        if i == 0:
            reward = 1
            if j == 2:
                reward += 2
            
        if i == 3 and j == 1:
            done = True
        else:
            done = False

        info = {}
        return state, reward, done, info

    def reset(self):
        self.game.reset()
        return self.game.known_grid

    def render(self):
        print(self.game.known_grid)
        print('----')


class DummyGame:
    def __init__(self):
        self.rows = 4
        self.cols = 2

        self.grid = [
            [1, 2],
            [3, 4],
            [5, 6], 
            [7, 8]
        ]

        self.known_grid = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
        ]
    
    def reveal(self, i, j):
        self.known_grid[i][j] = self.grid[i][j]
    
    def reset(self):
        self.known_grid = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
        ]


game = DummyGame()
env = MinesweeperEnv(game)
# print(env.action_space.sample())
# print(env.observation_space.sample())

# for i in range(20):
observation = env.reset()
for t in range(100):
    env.render()
    # print(observation)
    action = env.action_space.sample()
    # print(action)
    observation, reward, done, info = env.step(action)
    if done:
        print(f'Episode finished after {t+1} timesteps')
        break
env.close()



print('done')