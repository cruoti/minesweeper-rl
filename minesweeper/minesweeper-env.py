import random
from time import sleep
import gym
from gym import spaces
import pygame

from backend import EasyGame, MedGame, HardGame
from frontend import SPRITE_UNKNWN
from frontend import ScreenCell, ScreenField


class MinesweeperEnv(gym.Env):
    def __init__(self, game):
        self.game = game

        # required
        self.action_space = spaces.Discrete(self.game.rows * self.game.cols)
        # self.action_space = spaces.Box(low=0, high=1, shape=(self.game.rows, self.game.cols), dtype=int)
        self.observation_space = spaces.Box(low=0, high=10, shape=(self.game.rows, self.game.cols), dtype=int)

        # not required
        self.memory = set([])

    @property
    def known_grid(self):
        grid = self.game.create_empty_field(None, self.game.rows, self.game.cols)
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                if self.game.mine_field[i][j].is_known:
                    grid[i][j] = self.game.mine_field[i][j].value
                else:
                    grid[i][j] = -2
        return grid

    def step(self, action):
        i = action // self.game.cols
        j = action % self.game.cols 

        # i = random.randrange(0, self.game.rows)
        # j = random.randrange(0, self.game.cols)
        
        if (i, j) in self.memory:
            reward = -5
            done = False
            info = {}
            print(f'ALREADY CLICKED: {reward}')    
            return self.known_grid, reward, done, info
        self.memory.add((i, j))

        is_game_over = self.game.click_cell(i, j)

        if not is_game_over:
            reward = 1
            done = False
            info = {}
            print(f'GOOD CLICK: {reward}')
            return self.known_grid, reward, done, info
        else:
            done = True
            info = {}
            if self.game.is_won:
                reward = 1
                print(f'WON: {reward}')
            else:
                reward = -500
                print(f'LOST: {reward}')
            return self.known_grid, reward, done, info


    def reset(self):
        self.game.setup()
        return self.known_grid

    def render(self):
        for i in range(self.game.rows):
            for j in range(self.game.cols):
                rect = pygame.Rect(j*cell_width, i*cell_height, cell_width, cell_height)
                if self.game.mine_field[i][j].is_known:
                    sprite = ScreenCell.get_sprite(self.game.mine_field[i][j].value)
                else:
                    sprite = SPRITE_UNKNWN
                sprite = pygame.transform.scale(sprite, (cell_width, cell_height))
                screen.blit(sprite, rect)
        pygame.display.flip()


if __name__ == '__main__':
    game = HardGame()


    pygame.init()
    screen_height = 500
    screen_width = screen_height * 1.2
    screen = pygame.display.set_mode([screen_width, screen_height])

    cell_width = screen_width // game.cols
    cell_height = screen_height // game.rows

    screen.fill((255, 255, 255))


    env = MinesweeperEnv(game)
    # print(env.action_space.sample())
    # print(env.observation_space.sample())

    for i in range(200):
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
            sleep(0.1)
    env.close()

    pygame.quit()


    print('done')