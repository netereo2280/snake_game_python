import math
import random
import pygame
import time
import tkinter as tk
from tkinter import messagebox

pygame.init()
pygame.mixer.init()

pygame.mixer.Channel(0).play(pygame.mixer.Sound('wav\\aint_the_same.wav'))
pygame.mixer.Channel(0).set_volume(0.5)


class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(0,0,255)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # width/height of each cube
        i = self.pos[0] # current row
        j = self.pos[1] # current column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        # by multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it

        if eyes: # draws the eyes
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        



class snake(object):
    body = [] # list of cubes
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # the head will be the front of the snake
        self.body.append(self.head) # we will add head (which is a cube object) to our body list

        # these will represent the direction our snake is moving
        self.dirnx = 0
        self.dirny = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check if user hit the red x
                pygame.quit()

            keys = pygame.key.get_pressed() # see which keys are being pressed

            for key in keys: # loop through all the keys
                if keys[pygame.K_LEFT]:
                    if self.dirnx != 1:
                        self.dirnx = -1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    if self.dirnx != -1:
                        self.dirnx = 1
                        self.dirny = 0
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    if self.dirny != 1:
                        self.dirnx = 0
                        self.dirny = -1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    if self.dirny != -1:
                        self.dirnx = 0
                        self.dirny = 1
                        self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            
        for i, c in enumerate(self.body): # loop through every cube in our body
            p = c.pos[:] # this stores the cubes position on the grid
            if p in self.turns: # if the cubes current position is one where we turned
                turn = self.turns[p] # get the direction we should turn
                c.move(turn[0],turn[1]) # move our cube in that direction
                if i == len(self.body)-1: # if this is the last cube in our body remove the turn from the dict
                    self.turns.pop(p)
            """
            else: # if we are not turning the cube
                # if the cube reaches the edge of the screen we will make it appear on the opposite side
                
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) # if we haven't reached the edge just move in our currnet direction
            """


    def reset(self, pos):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('wav\\aint_the_same.wav'))
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 0


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # we need to know which side of the snake to add the cube to.
        # so we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        # we then set the cubes direction to the direction of the snake
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy
        
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('wav\\sound1.wav'))

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0: # for the first cube in the list we want to draw eyes
                c.draw(surface, True) # adding the true as an argument will tell us to draw eyes
            else:
                c.draw(surface) # otherwise we will just draw a cube

# redrawWindow
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # gives us distance between the lines

    x = 0 # keeps track of the current x
    y = 0 # keeps track of the current y
    for l in range(rows): # we will draw one vertical and one horizontal line each loop
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        # pygame.draw.line(surface, color, from, to)
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))

        

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0)) # fills the screen with black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface) # will draw our grid lines
    pygame.display.update() # updates the screen


def randomSnack(rows, item):

    positions = item.body # get all the positions of cubes in our snake

    while True: # keep generating random positions until we get a valid one
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            # this will check if the position we generated is occupied by the snake
            continue
        else:
            break
        
    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def message(msg,color):
    font_style = pygame.font.SysFont(None, 50)
    mesg = font_style.render(msg, True, color)
    win = pygame.display.set_mode((width, width))
    win.blit(mesg, [190, 210])


def main():
    global width, rows, s, snack
    t = 10
    width = 500 # width of our screen
    rows = 20 # amount of rows
    win = pygame.display.set_mode((width, width)) # creates our screen object
    s = snake((0,0,255), (10,10)) # creates a snake object
    pygame.display.set_caption('SNAKE GAME BY LONGMV')
    snack = cube(randomSnack(rows, s), color=(255,0,0))
    flag = True

    clock = pygame.time.Clock() # creating a clock object
    
    # STARTING MAIN LOOP
    while flag:
        pygame.time.delay(5)
        clock.tick(t)
        s.move()

        if pygame.mixer.Channel(0).get_busy() == False:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('wav\\aint_the_same.wav'))
            pygame.mixer.Channel(0).set_volume(0.5)

        if s.body[0].pos == snack.pos: # checks if the head collides with the snack
            if t < 20:
                clock.tick(t + 1)
            t = t + 1
            s.addCube() # adds a new cube to the snake
            snack = cube(randomSnack(rows, s), color=(255,0,0)) # creates a new snack object
            pygame.display.set_caption('SNAKE GAME BY LONGMV')
            
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                # this will check if any of the positions in our body list overlap
                pygame.mixer.Channel(0).stop()
                time.sleep(2)
                message('you lost', (255, 0, 0))
                pygame.display.update()
                time.sleep(1)
                message_box('You Lost!', 'Score: %d\nPlay again...' % (len(s.body)-1))
                s.reset((10,10))
                t = 10
                break

        redrawWindow(win)

main()