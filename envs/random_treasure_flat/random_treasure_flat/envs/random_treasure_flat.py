import random
import time
from tkinter import *

import gym
import numpy as np


class RandomTreasureFlat(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.NO_MOVE = 4
        self.num_actions = 5
        self.MAX_STEPS = 25
        self.arena_size = 16

        self.reset()
        # print('shape is' + str(self.state.shape))
        # print('shape 0 is' + str(self.state.shape[0]))
        self.action_space = gym.spaces.Discrete(5)
        self.observation_space = gym.spaces.Box(low=0, high=15, shape=self.state.shape,  dtype=np.uint8)

        #self.box_pixels = 50
        #self.init_tkinter()

    def get_action_meanings(self):
        return ['UP', 'RIGHT', 'DOWN', 'LEFT', 'NO_MOVE']

    def init_tkinter(self):
        wh = self.arena_size * self.box_pixels
        self.root = Tk()
        self.frame = Frame(self.root, width=wh, height=wh)
        self.frame.pack(expand=True, fill=BOTH)
        self.canvas = Canvas(self.frame, bg='grey', width=wh, height=wh)
        self.canvas.pack(expand=True, fill=BOTH)

    def step(self, action):
        self.steps += 1
        done = False
        self.move_box(0, 1, action)

        # convict = self.state[0:1][0]
        # loot = self.state[1:2][0]

        convict_x = self.state[0]
        convict_y = self.state[1]
        loot_x = self.state[2]
        loot_y = self.state[3]
        #reward = 0
        reward = self.distance_score(convict_x, convict_y, loot_x, loot_y)
        if self.check_things_on_same_spot(convict_x, convict_y, loot_x, loot_y):
            reward += 10
            # done = True

        if self.steps >= self.MAX_STEPS:
            done = True
            # reward = -30

        #print('reward=' + str(reward))

        info = {'reward': reward, 'mystr': 'uuuctest'}
        return self.state, reward, done, info

    def reset(self):
        # self.state = np.array([(8, 7), (3, 3), (2, 12), (13, 3), (13, 11), (6, 7), (8, 5), (8, 10)])
        # possible_treasure_locations = [(10, 9), (6, 5), (10, 5), (6, 9)]
        # possible_treasure_locations = [(10, 10), (5, 4)]
        # treasure = random.choice(possible_treasure_locations)
        self.state = np.array([8, 7, 10, 9])
        self.steps = 0
        return self.state

    def render(self, mode='human', close=False):
        print('state=' + str(self.state))
        pass

    # def render(self, mode='human', close=False):
    #     self.canvas.delete("all")
    #
    #     convict_x = self.state[0]
    #     convict_y = self.state[1]
    #     loot_x = self.state[2]
    #     loot_y = self.state[3]
    #
    #     self.render_box(convict_x, convict_y, 'orange')
    #     self.render_box(loot_x, loot_y, 'darkgreen')
    #     self.root.update()
    #
    #     if close:
    #         self.root.destroy()
    #     else:
    #         time.sleep(.4)

    def can_move(self, x_ix, y_ix, action):
        return (action == self.UP and self.state[y_ix] > 0) or \
               (action == self.RIGHT and self.state[x_ix] < self.arena_size - 1) or \
               (action == self.DOWN and self.state[y_ix] < self.arena_size - 1) or \
               (action == self.LEFT and self.state[x_ix] > 0)

    def render_box(self, position_x, position_y, color):
        x1 = position_x * self.box_pixels
        x2 = (position_x + 1) * self.box_pixels
        y1 = position_y * self.box_pixels
        y2 = (position_y + 1) * self.box_pixels
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    def distance_score(self, convict_x, convict_y, loot_x, loot_y):
        max_distance = self.arena_size - 1
        moves_x = np.abs(convict_x - loot_x)
        moves_y = np.abs(convict_y - loot_y)
        return 0.05 * (max_distance - moves_x) + 0.05 * (max_distance - moves_y)

    def move_box(self, x_ix, y_ix, action):
        if action == self.NO_MOVE or not self.can_move(x_ix, y_ix, action):
            return

        if action == self.UP:
            self.state[y_ix] -= 1
        elif action == self.RIGHT:
            self.state[x_ix] += 1
        elif action == self.DOWN:
            self.state[y_ix] += 1
        else:  # action == self.LEFT:
            self.state[x_ix] -= 1

    def check_things_on_same_spot(self, x1_ix, y1_ix, x2_ix, y2_ix):
        return x1_ix == x2_ix and y1_ix == y2_ix
