import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import time
import random


class FixedNumber(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.UP = 0
        self.DOWN = 1
        self.NO_ACTION = 2
        self.num_actions = 3
        self.MAX_STEPS = 12
        self.GOAL = 5
        self.HIGH = 10

        self.reset()
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=np.array([0]), high=np.array([10]), dtype=np.uint8)
        #self.observation_space = gym.spaces.Box(low=0, high=10, shape=(1,), dtype=np.uint8)
        #shape =(1,),
        #self.observation_space = gym.spaces.Box(low=np.array([0]), high=np.array([10]), dtype=np.uint8)

    def step(self, action):
        #print('s=' + str(self.state) + ' a=' + str(action))

        self.steps += 1
        done = False
        if action == self.UP and self.state[0] < self.HIGH:
            self.state[0] += 1
        if action == self.DOWN and self.state[0] > 0:
            self.state[0] -= 1

        reward = 0
        if self.state[0] == self.GOAL:
            done = True
            reward = 100
        elif self.steps >= self.MAX_STEPS:
            done = True
            reward = -100

        # reward = 0
        # if self.state[0] == self.GOAL:
        #     reward = 1
        # if self.steps >= self.MAX_STEPS:
        #     done = True

        info = {}
        return self.state, reward, done, info

    def reset(self):
        self.state = np.array([random.choice([2, 3, 7])])
        self.steps = 0
        return self.state

    def render(self, mode='human', close=False):
        pass
