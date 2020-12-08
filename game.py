import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
    rows = 20
    w = 500
    colors = [(105, 181, 78), (68, 117, 113), (68, 74, 117), (117, 68, 68), (237, 173, 173), (203, 232, 160)]
    def __init__(self,start,dirnx=1,dirny=0,color= random.choice(colors)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = random.choice(colors)

        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # change position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # width/height of cube
        i = self.pos[0] # current row
        j = self.pos[1] # current column

        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2)) # multiply row and column value of cube to know where to locate
        if eyes: #draw eyes on first cube
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        



class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # head is front of snake
        self.body.append(self.head) # add head to body
        self.dirnx = 0 # direction of snake
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # check if user hit red x
                pygame.quit()

            keys = pygame.key.get_pressed() # which keys are pressed

            
            for key in keys: # loops through all keys
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body): # loop every cube in body
            p = c.pos[:] # stores cube position on grid
            if p in self.turns: # if current position is where we turned
                turn = self.turns[p] # gets the direction turned
                c.move(turn[0],turn[1]) # move cube to the direction
                if i == len(self.body)-1: # if it's the last cube on the body, remove from dict
                    self.turns.pop(p)
            else: # if we are not turning the cube, make the cube appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny) # if the snake didn't reach the edge, keep on going in the direction
        

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        # which side to add cube, check direction 

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].dirnx = dx # cube go the same direction as snake
        self.body[-1].dirny = dy
        

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0: # draw eyes in the first cube
                c.draw(surface, True) # true statement tells it to draw eyes
            else:
                c.draw(surface) # if not draw a cube


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # distance between the lines

    x = 0 # keeps track of x
    y = 0 # keeps track of y
    for l in range(rows): # horizontal, vertical line each loop
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
        

def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0)) #fills screen w/black
    s.draw(surface) # grid lines
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update() #updates screen


def randomSnack(rows, item):

    positions = item.body # get position of cubes of snake

    while True: # makes positions that the snake is not on
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue # check if snake is there
        else:
            break
        
    return (x,y)


def main():
    global width, rows, s, snack, colors,yes
    colors = [(105, 181, 78), (68, 117, 113), (68, 74, 117), (117, 68, 68), (237, 173, 173), (203, 232, 160)]
    width = 500 #width of screen
    rows = 20 #s of rows
    win = pygame.display.set_mode((width, width)) #creates a screen
    s = snake(random.choice(colors), (10,10))# makes a snake
    snack = cube(randomSnack(rows, s), color=(0,255,0)) #
    flag = True

    clock = pygame.time.Clock() # timer
    
    while flag: #main loop
        pygame.time.delay(50) #delay the game
        clock.tick(10) # 10 Fps
        s.move()
        if s.body[0].pos == snack.pos: # check if snake ate snack
            s.addCube() #add new cube to the snake
            snack = cube(randomSnack(rows, s), color= random.choice(colors)) #makes new snake

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])): #check if snake overlap
                print('You Lost!', "try again" 'Score: ', len(s.body))
                answer = input("Do you want to play again?(yes?): ")
                if answer.lower()== "yes":
                    s.reset((10,10))
                else: 
                    answer = input("Do you want to play again?(yes?): ")
                break

            
        redrawWindow(win)

main()