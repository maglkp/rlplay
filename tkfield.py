from tkinter import *
from numpy import random
import time
import curses
import numpy as np


# https://stackoverflow.com/questions/25430786/moving-balls-in-tkinter-canvas/25431690#25431690
# https://gordonlesti.com/use-tkinter-without-mainloop/
class TkField:
    def __init__(self):
        self.UP = 0
        self.RIGHT = 1
        self.DOWN = 2
        self.LEFT = 3
        self.NO_MOVE = 4
        self.num_actions = 5

        self.arena_size = 16
        self.box_pixels = 50
        wh = self.arena_size * self.box_pixels
        self.root = Tk()

        self.frame = Frame(self.root, width=wh, height=wh)
        self.frame.pack(expand=True, fill=BOTH)

        self.canvas = Canvas(self.frame, bg='grey', width=wh, height=wh)
        self.canvas.pack(expand=True, fill=BOTH)

        self.robots = [(3, 3), (2, 12), (13, 3), (13, 11), (11, 3), (11, 11), (6, 7), (8, 5), (8, 9), (8, 3), (8, 11)]
        self.loot = (11, 9)
        self.convict = (8, 7)
        self.steps = 0
        self.loot_boxes_collected = 0

    def loop(self):
        # Button(self.root, text="Quit", command=self.root.destroy).pack()
        self.root.mainloop()

    def render(self):
        self.canvas.delete("all")

        for robot in self.robots:
            self.render_box(robot, 'navy')
        self.render_box(self.convict, 'orange')
        self.render_box(self.loot, 'darkgreen')
        self.root.update()

        # self.canvas.pack(expand=True, fill=BOTH)

    def render_box(self, position, color):
        x1 = position[0] * self.box_pixels
        x2 = (position[0] + 1) * self.box_pixels
        y1 = position[1] * self.box_pixels
        y2 = (position[1] + 1) * self.box_pixels
        # print((x1, y1, x2, y2))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    def step_manual(self, action):
        self.robots = [self.move_box(robot) for robot in self.robots]
        self.convict = self.move_box_manual(self.convict, action)
        if self.check_things_on_same_spot(self.loot, self.convict):
            self.loot_boxes_collected += 1
            loot_pos = int(self.arena_size / 4)
            h = int(self.arena_size / 2)
            x_wind = random.randint(h)
            y_wind = random.randint(h)
            self.loot = (loot_pos + x_wind, loot_pos + y_wind)

        return self.check_caught()

    def check_caught(self):
        return any(self.check_things_touch(r, self.convict) for r in self.robots)

    def check_things_on_same_spot(self, r1, r2):
        return r1[0] == r2[0] and r1[1] == r2[1]

    def check_things_touch(self, r1, r2):
        diff1 = np.abs(r1[0] - r2[0])
        diff2 = np.abs(r1[1] - r2[1])
        return (diff1 <= 1 and diff2 == 0) or (diff2 <= 1 and diff1 == 0)

    def step(self):
        self.robots = [self.move_box(robot) for robot in self.robots]
        self.convict = self.move_box(self.convict)

    def move_box_manual(self, box, action):
        if action == self.NO_MOVE or not self.not_blocked_by_wall(box, action):
            return box

        if action == self.UP:
            return box[0], box[1] - 1
        elif action == self.RIGHT:
            return box[0] + 1, box[1]
        elif action == self.DOWN:
            return box[0], box[1] + 1
        else:  # action == self.LEFT:
            return box[0] - 1, box[1]

    def move_box(self, box):
        action = random.randint(self.num_actions)
        if action == self.NO_MOVE or not self.not_blocked_by_wall(box, action):
            return box

        if action == self.UP:
            return box[0], box[1] - 1
        elif action == self.RIGHT:
            return box[0] + 1, box[1]
        elif action == self.DOWN:
            return box[0], box[1] + 1
        else:  # action == self.LEFT:
            return box[0] - 1, box[1]

    def not_blocked_by_wall(self, box, action):
        return (action == self.UP and box[1] > 0) or \
               (action == self.RIGHT and box[0] < self.arena_size - 1) or \
               (action == self.DOWN and box[1] < self.arena_size - 1) or \
               (action == self.LEFT and box[0] > 0)


field = TkField()

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)

stdscr.addstr(0, 10, "Hit 'q' to quit")
stdscr.refresh()

field.render()
key = ''
end = False
while key != ord('q') and not end:
    key = stdscr.getch()
    stdscr.addch(20, 25, key)
    stdscr.refresh()

    if key == curses.KEY_UP:
        end = field.step_manual(field.UP)
    elif key == curses.KEY_DOWN:
        end = field.step_manual(field.DOWN)
    elif key == curses.KEY_LEFT:
        end = field.step_manual(field.LEFT)
    elif key == curses.KEY_RIGHT:
        end = field.step_manual(field.RIGHT)

    field.render()

curses.endwin()

# field.render()
# time.sleep(1)
# field.step()
# field.render()

# field.loop()

# time.sleep(1)

# for i in range(20):    
#     field.render()
#     time.sleep(1)
