import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

class EntEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.NO_MOVE = 4
        self.num_actions = 5
        self.MAX_STEPS = 10
        self.arena_size = 16

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(8, 2), dtype=np.uint8)
        self.state = None
        self.steps = None
        #print("Init ENT")

    def step(self, action):
        self.steps += 1        
        done = False
        reward = 1

        self.state = self.move_all(action)
        if self.check_caught():
            done = True
            reward = 0
        elif self.steps >= self.MAX_STEPS:
            done = True
            reward = 100

        info = {}
        return np.array(self.state), reward, done, info

    def reset(self):
        #print("RST ENT")
        self.state = [(8, 7), (3, 3), (2, 12), (13, 3), (13, 11), (6, 7), (8, 5), (8, 10)]
        self.steps = 0
        return np.array(self.state)

    def render(self, mode='human', close=False):
        pass

    def can_move(self, box, action):
        return (action == self.UP and box[1] > 0) or \
               (action == self.RIGHT and box[0] < self.arena_size - 1) or \
               (action == self.DOWN and box[1] < self.arena_size - 1) or \
               (action == self.LEFT and box[0] > 0)

    def move_all(self, action):
        convict = self.state[0:1]
        robots =  self.state[1:]
        robots = [self.move_box_random(robot) for robot in robots]
        convict[0] = self.move_box(convict[0], action)
        return convict + robots

    def move_box(self, box, action):
        if action == self.NO_MOVE or not self.can_move(box, action):
            return box

        if action == self.UP:
            return (box[0], box[1] - 1)
        elif action == self.RIGHT:
            return (box[0] + 1, box[1])
        elif action == self.DOWN:
            return (box[0], box[1] + 1)
        else:  # action == self.LEFT:
            return (box[0] - 1, box[1])

    def move_box_random(self, box):
        action = np.random.randint(self.num_actions)
        if action == self.NO_MOVE or not self.can_move(box, action):
            return box

        if action == self.UP:
            return (box[0], box[1] - 1)
        elif action == self.RIGHT:
            return (box[0] + 1, box[1])
        elif action == self.DOWN:
            return (box[0], box[1] + 1)
        else:  # action == self.LEFT:
            return (box[0] - 1, box[1])

    def check_caught(self):
        convict = self.state[0]
        robots =  self.state[1:]
        return any(self.check_things_touch(r, convict) for r in robots)        

    def check_things_touch(self, r1, r2):
        diff1 = np.abs(r1[0] - r2[0])
        diff2 = np.abs(r1[1] - r2[1])
        return (diff1 <= 1 and  diff2 == 0) or (diff2 <= 1 and diff1 == 0)
