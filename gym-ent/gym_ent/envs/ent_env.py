import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from tkinter import *
import time

class EntEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.NO_MOVE = 4
        self.num_actions = 5
        self.MAX_STEPS = 80
        self.arena_size = 16

        self.state = None
        self.steps = None
        self.reset()
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(self.state.shape[0], 2), dtype=np.uint8)
        self.loot_boxes_collected = 0

        self.box_pixels = 50
        self.init_tkinter()

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
        reward = 0

        self.state = self.move_all(action)

        # add a fraction of the reward closer to loot they are
        # and more distant from closest robot
        convict = self.state[0:1][0]
        loot = self.state[1:2][0]
        if self.check_things_on_same_spot(loot, convict):
            #print("loot box collected")
            self.loot_boxes_collected += 1
            loot_pos = int(self.arena_size / 4)
            h = int(self.arena_size / 2)
            x_wind = np.random.randint(h)
            y_wind = np.random.randint(h)
            loot = (loot_pos + x_wind, loot_pos + y_wind)
            reward = 1

        self.state[1] = loot
        if self.check_caught():
            done = True
            reward = -30
        elif self.steps >= self.MAX_STEPS:
            done = True
            reward = self.loot_boxes_collected * 2 + 1

        info = {}
        return np.array(self.state), reward, done, info

    def reset(self):
        #self.root.destroy()
        #self.init_tkinter()
        #print("RST ENT")
        #self.state = np.array([(8, 7), (3, 3), (2, 12), (13, 3), (13, 11), (6, 7), (8, 5), (8, 10)])
        self.state = np.array([(8, 7), (11, 9), (3, 3), (2, 12), (13, 3), \
                                (13, 11), (11, 3), (11, 11), (6, 7), \
                                (8, 5), (8, 9), (8, 3), (8, 11)])

        self.loot_boxes_collected = 0
        self.steps = 0
        return np.array(self.state)

    def render(self, mode='human', close=False):
        self.canvas.delete("all")

        convict = self.state[0:1]
        loot_box = self.state[1:2]
        robots =  self.state[2:]
        for robot in robots:
            self.render_box(robot, 'navy')
        self.render_box(convict[0], 'orange')
        self.render_box(loot_box[0], 'darkgreen')
        self.root.update()

        if(close):
            self.root.destroy()
        else:
            time.sleep(.4)

    def can_move(self, box, action):
        return (action == self.UP and box[1] > 0) or \
               (action == self.RIGHT and box[0] < self.arena_size - 1) or \
               (action == self.DOWN and box[1] < self.arena_size - 1) or \
               (action == self.LEFT and box[0] > 0)

    def render_box(self, position, color):
        x1 = position[0] * self.box_pixels
        x2 = (position[0] + 1) * self.box_pixels
        y1 = position[1] * self.box_pixels
        y2 = (position[1] + 1) * self.box_pixels
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    def move_all(self, action):
        convict = self.state[0:1]
        loot_box = self.state[1:2]
        robots =  self.state[2:]
        robots = np.array([self.move_box_random(robot) for robot in robots])
        convict[0] = np.array(self.move_box(convict[0], action))
        return np.concatenate((convict, loot_box, robots))

    def move_box(self, box, action):
        if action == self.NO_MOVE or not self.can_move(box, action):
            return box

        if action == self.UP:
            return box[0], box[1] - 1
        elif action == self.RIGHT:
            return box[0] + 1, box[1]
        elif action == self.DOWN:
            return box[0], box[1] + 1
        else:  # action == self.LEFT:
            return box[0] - 1, box[1]

    def move_box_random(self, box):
        action = np.random.randint(self.num_actions)
        if action == self.NO_MOVE or not self.can_move(box, action):
            return box

        if action == self.UP:
            return box[0], box[1] - 1
        elif action == self.RIGHT:
            return box[0] + 1, box[1]
        elif action == self.DOWN:
            return box[0], box[1] + 1
        else:  # action == self.LEFT:
            return box[0] - 1, box[1]

    def check_caught(self):
        convict = self.state[0]
        robots =  self.state[1:]
        return any(self.check_things_touch(r, convict) for r in robots)

    def check_things_on_same_spot(self, r1, r2):
        return r1[0] == r2[0] and r1[1] == r2[1]

    def check_things_touch(self, r1, r2):
        diff1 = np.abs(r1[0] - r2[0])
        diff2 = np.abs(r1[1] - r2[1])
        return (diff1 <= 1 and  diff2 == 0) or (diff2 <= 1 and diff1 == 0)
