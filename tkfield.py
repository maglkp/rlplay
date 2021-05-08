from tkinter import *
from numpy import random
import time

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

        self.canvas = Canvas(self.frame, bg='white', width=wh, height=wh)
        self.canvas.pack(expand=True, fill=BOTH)

        self.robots = [(2, 2), (2, 13), (13, 2), (13, 13), (4, 7)]
        self.convict = (8, 7)

    def loop(self):
        # Button(self.root, text="Quit", command=self.root.destroy).pack()
        self.root.mainloop()

    def render(self):
        self.canvas.delete("all")

        for robot in self.robots:
            self.render_box(robot, 'blue')
        self.render_box(self.convict, 'red')
        self.root.update()

        #self.canvas.pack(expand=True, fill=BOTH)

    def render_box(self, position, color):
        x1 = position[0] * self.box_pixels
        x2 = (position[0] + 1) * self.box_pixels
        y1 = position[1] * self.box_pixels
        y2 = (position[1] + 1) * self.box_pixels
        #print((x1, y1, x2, y2))
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)

    def step(self):
        self.robots = [self.move_box(robot) for robot in self.robots]
        self.convict = self.move_box(self.convict)

    def move_box(self, box):
        action = random.randint(self.num_actions)
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

    def can_move(self, box, action):
        return (action == self.UP and box[1] > 0) or \
               (action == self.RIGHT and box[0] < self.arena_size - 1) or \
               (action == self.DOWN and box[1] < self.arena_size - 1) or \
               (action == self.LEFT and box[0] > 0)


field = TkField()

field.render()
time.sleep(1)
field.step()
field.render()
time.sleep(1)
field.step()
field.render()

#field.loop()

time.sleep(1)

# for i in range(20):    
#     field.render()
#     time.sleep(1)
