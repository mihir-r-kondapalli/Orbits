#!/usr/bin/env python

import pygame
from pygame.locals import *
import time
import random
import math
import os

pygame.init()
WINDOW_W = 1200
WINDOW_H = 750
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Orbits")

BLAST_SOUND = pygame.mixer.Sound('GameSounds/laser.ogg')
EXPLO_SOUND = pygame.mixer.Sound('GameSounds/explo.ogg')
BLACK_HOLE_SOUND = pygame.mixer.Sound('GameSounds/blackhole.ogg')
WHITE_HOLE_SOUND = pygame.mixer.Sound('GameSounds/whitehole.ogg')
WORM_HOLE_SOUND = pygame.mixer.Sound('GameSounds/warp.ogg')
APPEAR_SOUND = pygame.mixer.Sound('GameSounds/teleport.ogg')
RADAR_SOUND = pygame.mixer.Sound('GameSounds/radar.ogg')
SPACE_SOUND = pygame.mixer.Sound('GameSounds/spacesound.ogg')
CLOSE_SOUND = pygame.mixer.Sound('GameSounds/closesound.ogg')
WIN_SOUND = pygame.mixer.Sound('GameSounds/win.ogg')
CLICK_SOUND = pygame.mixer.Sound('GameSounds/click.ogg')

def num_Files(dirName):
    numF = os.listdir(dirName)
    number_files = len(numF)-1

    return number_files

def new_song():
    global si
    global songs
    
    si = si+1

    if si>(len(songs)-1):
        si = 1
        random.shuffle(songs)
    
    pygame.mixer.music.load(songs[si])
    pygame.mixer.music.play()

AMNTSONGS = num_Files('PlayList')

songs = []

for i in range(0, AMNTSONGS):
    songs.append('Playlist/song_'+str(i+1)+'.mp3')

SONG_END = pygame.USEREVENT + 1

pygame.mixer.music.set_endevent(SONG_END)
pygame.mixer.music.load(songs[1])

pygame.mixer.music.play(-1)
pygame.mixer.music.pause()

random.shuffle(songs)

si = 1

songsAct = False


game_over = False

clock = pygame.time.Clock()

objects = []

G = 1

HEALTH = 8

NUMPL = 5

font = pygame.font.SysFont('Arial', 20)

NUM_STARS = 100

playerNums = [1, 0, 0, 2]

avAb = [1, 1, 1, 1, 1, 1, 1]

class Planet(object):
    def __init__(self, xpos, ypos, mass, size, init_vect):
        
        self.xpos = xpos
        self.ypos = ypos
        self.mass = mass
        self.size = size

        self.initX = 0
        self.initY = 0

        self.health = 0

        self.r = int(random.uniform(100, 225))
        self.g = int(random.uniform(100, 225))
        self.b = int(random.uniform(100, 225))

        self.player = 0

        self.velocity = init_vect

        self.ID = False

    def add_velocity(self, v, a):
        diffX = self.velocity[0]*math.cos(self.velocity[1])
        diffY = self.velocity[0]*math.sin(self.velocity[1])

        diffX+=v*math.cos(a)
        diffY+=v*math.sin(a)
        
        self.velocity[0] = math.sqrt(pow(diffX, 2)+pow(diffY, 2))

        if diffX==0:
            diffX = 0.00000001

        self.velocity[1] = math.atan(diffY/diffX)

        if diffX<0:
            self.velocity[1]+=math.pi

    def move(self):
        global G
        #self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        #self.ypos+=self.velocity[0]*math.sin(self.velocity[1])
        G = 1

    def bounds(self):
        col = False
        
        if self.xpos<self.size:
            col = True
        if self.xpos>WINDOW_W-self.size:
            col = True
        if self.ypos<self.size :
            col = True
        if self.ypos>WINDOW_H-self.size:
            col = True

    def draw(self):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.xpos), int(self.ypos)), self.size)

    def collide(self):
        global G
        G = 1

    def print(self):
        print(self.velocity)

    def isOut(self):
        out = False
        
        if self.xpos<self.size:
            out = True
        if self.xpos>WINDOW_W-self.size:
            out = True
        if self.ypos<self.size :
            out = True
        if self.ypos>WINDOW_H-self.size:
            out = True

        return out

class Projectile(Planet):
    def __init__(self, xpos, ypos, mass, size, init_vect, player):
        
        self.TRAIL = 8
        self.health = 0

        self.ID = False

        self.xpos = float(xpos)
        self.ypos = float(ypos)
        self.mass = mass
        self.size = size

        self.player = player

        self.xpoints = []
        self.ypoints = []

        self.initX = -500*player
        self.initY = -500*player

        self.spd = 5

        for i in range(0, self.TRAIL+1):
            self.xpoints.append(self.xpos)
            self.ypoints.append(self.ypos)

        self.r = int(random.uniform(100, 225))
        self.g = int(random.uniform(100, 225))
        self.b = int(random.uniform(100, 225))

        self.rchange = (self.r-10)//self.TRAIL
        self.gchange = (self.g-10)//self.TRAIL
        self.bchange = (self.b-10)//self.TRAIL

        self.velocity = init_vect

    def move(self):
        self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        self.ypos+=self.velocity[0]*math.sin(self.velocity[1])

        for i in range(0, self.TRAIL):
            self.xpoints[i] = self.xpoints[i+1]
            self.ypoints[i] = self.ypoints[i+1]

        self.xpoints[self.TRAIL] = self.xpos
        self.ypoints[self.TRAIL] = self.ypos

    def bounds(self):
        col = False
        
        if self.xpos<self.size:
            col = True
        if self.xpos>WINDOW_W-self.size:
            col = True
        if self.ypos<self.size :
            col = True
        if self.ypos>WINDOW_H-self.size:
            col = True

    def collide(self):
        global objects
        
        xdiff = 0
        ydiff = 0

        dist = 0

        close = False

        size = len(objects)

        for i in range(0, size):
            xdiff = abs(self.xpos-objects[i].xpos)
            ydiff = abs(self.ypos-objects[i].ypos)

            dist = math.sqrt(pow(xdiff, 2)+pow(ydiff, 2))

            if(dist<(self.size+objects[i].size) and (self.player!=objects[i].player and objects[i].player!=0)):
                EXPLO_SOUND.play()
                
                self.health-=1
                objects[i].health-=1
                self.xpos = self.initX
                self.ypos = self.initY
                objects[i].xpos = objects[i].initX
                objects[i].ypos = objects[i].initY
                self.velocity = [0.0, 0.0]
                self.mass = 0

                if objects[i].player==-1:
                    objects[i].mass = 0
                    time.sleep(0.5)

                else:
                    time.sleep(0.75)

    def draw(self):
        for i in range(0, self.TRAIL+1):
            pygame.draw.circle(screen, ((i*self.rchange), (i*self.gchange),
                               (i*self.bchange)), (int(self.xpoints[i]),
                                                      int(self.ypoints[i])),
                                                          self.size)
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.xpos), int(self.ypos)), self.size)

class ProjectileB(Projectile):
    def __init__(self, xpos, ypos, mass, size, init_vect, player):
        super().__init__(xpos, ypos, mass, size, init_vect, player)
    
    def add_velocity(self, v, a):
        global G
        G = 1

class Player(Planet):
    def __init__(self, xpos, ypos, mass, size, init_vect, left, right, up, down, shoot, shootB, shootC, shootD, shootE, shootF, shootG, radar, player):

        self.TRAIL = 8
        self.LIM = 2
        self.SHOOT_V = 3
        self.health = HEALTH

        self.initX = xpos
        self.initY = ypos

        self.added_v = 0.0

        self.xpos = float(xpos)
        self.ypos = float(ypos)
        self.mass = mass
        self.size = size

        self.xpoints = []
        self.ypoints = []

        self.spd = 0.1

        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.shoot = shoot
        self.shootB = shootB
        self.shootC = shootC
        self.shootD = shootD
        self.shootE = shootE
        self.shootF = shootF
        self.shootG = shootG
        self.radar = radar

        self.add_time = time.time()
        self.at = 5
        self.add_timeB = time.time()
        self.atB = 10
        self.add_timeC = time.time()
        self.atC = 20
        self.add_timeD = time.time()
        self.atD = 8
        self.add_timeE = time.time()
        self.atE = 35
        self.add_timeF = time.time()
        self.atF = 25
        self.add_timeG = time.time()
        self.atG = 40

        self.player = player

        self.ID = False

        for i in range(0, self.TRAIL+1):
            self.xpoints.append(self.xpos)
            self.ypoints.append(self.ypos)

        self.r = int(random.uniform(100, 225))
        self.g = int(random.uniform(100, 225))
        self.b = int(random.uniform(100, 225))

        self.rchange = (self.r-10)//self.TRAIL
        self.gchange = (self.g-10)//self.TRAIL
        self.bchange = (self.b-10)//self.TRAIL

        self.velocity = init_vect

    def move(self):
        global objects

        self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        self.ypos+=self.velocity[0]*math.sin(self.velocity[1])
        
        if self.health>0:
            key = pygame.key.get_pressed()
            if key[self.left]:
                self.velocity[1]-=0.02
            if key[self.right]:
                self.velocity[1]+=0.02
            if key[self.up]:
                if self.added_v>=self.LIM:
                    self.added_v = self.LIM
                else:
                    self.velocity[0]+=self.spd
                    self.added_v+=self.spd
            if key[self.down]:
                if self.added_v<=0:
                    self.added_v=0
                else:
                    self.velocity[0]-=self.spd
                    self.added_v-=self.spd

            if self.xpos>WINDOW_W-self.size:
                self.xpos = WINDOW_W-self.size
            if self.xpos<self.size:
                self.xpos = self.size
            if self.ypos>WINDOW_H-self.size:
                self.ypos = WINDOW_H-self.size
            if self.ypos<self.size:
                self.ypos = self.size

            if not(key[self.radar]):
                if key[self.shoot] and time.time()-self.add_time>self.at:
                    objects.append(Projectile(self.xpos, self.ypos, 10, 5, [self.velocity[0]+self.SHOOT_V, self.velocity[1]], self.player))
                    objects[len(objects)-1].move()
                    objects[len(objects)-1].move()
                    BLAST_SOUND.play()
                    self.add_time = time.time()

                if key[self.shootB] and (time.time()-self.add_timeB>self.atB and self.velocity[0]>0.4) and avAb[0]>0:
                    objects.append(ProjectileB(self.xpos, self.ypos, 0, 5, [self.velocity[0], self.velocity[1]], self.player))
                    objects[len(objects)-1].move()
                    if avAb[0]==1:
                        BLAST_SOUND.play()
                    self.add_timeB = time.time()

                if key[self.shootC] and time.time()-self.add_timeC>self.atC and avAb[1]>0:
                    objects.append(Projectile(self.xpos, self.ypos, 10, 5, [1, self.velocity[1]], self.player))
                    objects[len(objects)-1].move()
                    if avAb[1]==1:
                        BLAST_SOUND.play()
                    self.add_timeC = time.time()

                if key[self.shootD] and time.time()-self.add_timeD>self.atD and avAb[2]>0:
                    objects.append(BlackHole(self.xpos, self.ypos, 250, 15, [-10, self.velocity[1]]))
                    for i in range(0, 5):
                        objects[len(objects)-1].place_move()
                    if avAb[2]==1:
                        BLACK_HOLE_SOUND.play()
                    self.add_timeD = time.time()
                if key[self.shootE] and time.time()-self.add_timeE>self.atE and avAb[3]>0:
                    objects.append(WhiteHole(self.xpos, self.ypos, 250, 15, [-10, self.velocity[1]]))
                    for i in range(0, 5):
                        objects[len(objects)-1].place_move()
                    if avAb[3]==1:
                        WHITE_HOLE_SOUND.play()
                    self.add_timeE = time.time()

                if key[self.shootF] and time.time()-self.add_timeF>self.atF and avAb[4]>0:
                    objects.append(Projectile(self.xpos, self.ypos, 150, 10, [self.velocity[0]+3, self.velocity[1]], self.player))
                    objects[len(objects)-1].move()
                    objects[len(objects)-1].move()
                    objects[len(objects)-1].move()
                    objects[len(objects)-1].move()
                    objects[len(objects)-1].move()
                    if avAb[4]==1:
                        BLAST_SOUND.play()
                    self.add_timeF = time.time()

                if key[self.shootG] and time.time()-self.add_timeG>self.atG and avAb[5]>0:
                    objects.append(Void(self.xpos, self.ypos, 80, 5, [-10, self.velocity[1]]))
                    for i in range(0, 5):
                        objects[len(objects)-1].place_move()
                    if avAb[5]==1:
                        WORM_HOLE_SOUND.play()
                    self.add_timeG = time.time()
            else:
                self.short_dist()
            

        for i in range(0, self.TRAIL):
            self.xpoints[i] = self.xpoints[i+1]
            self.ypoints[i] = self.ypoints[i+1]

        self.xpoints[self.TRAIL] = self.xpos
        self.ypoints[self.TRAIL] = self.ypos

    def bounds(self):
        colX = False
        colY = False
        
        if self.xpos==self.size:
            colX = True
        elif self.xpos==WINDOW_W-self.size:
            colX = True
        elif self.ypos==self.size :
            colY = True
        elif self.ypos==WINDOW_H-self.size:
            colY = True
        else:
            colX = False
            colY = False

        if colX:
            self.velocity = [0.1, math.pi-self.velocity[1]]

        if colY:
            self.velocity = [0.1, 2*math.pi-self.velocity[1]]

    def collide(self):
        global objects
        
        xdiff = 0
        ydiff = 0

        dist = 0

        close = False
        
        for i in range(0, len(objects)):
            xdiff = abs(self.xpos-objects[i].xpos)
            ydiff = abs(self.ypos-objects[i].ypos)

            dist = math.sqrt(pow(xdiff, 2)+pow(ydiff, 2))

            if(dist<(self.size+objects[i].size) and (self.player!=objects[i].player and objects[i].player!=0)):
                EXPLO_SOUND.play()

                self.health-=1
                objects[i].health-=1
                self.xpos = self.initX
                self.ypos = self.initY
                objects[i].xpos = objects[i].initX
                objects[i].ypos = objects[i].initY

                if objects[i].player==-1 and objects[i].mass!=0:
                    objects[i].mass = 0

                    time.sleep(0.5)

                else:
                    time.sleep(0.75)

    def short_dist(self):
        LINE_LENGTH = 30

        dists = []

        for i in range(0, len(objects)):
            diffX = abs(self.xpos-objects[i].xpos)
            diffY = abs(self.ypos-objects[i].ypos)

            dist = math.sqrt(pow(diffX, 2)+pow(diffY, 2))

            if dist<10**-17:
                dist = 10**17

            dists.append(dist)

        index = dists.index(min(dists))

        pygame.draw.line(screen, (255, 255, 255), (int(self.xpos), int(self.ypos)), (int(objects[index].xpos), int(objects[index].ypos)), 1)

        pygame.draw.line(screen, (255, 0, 0), (int(self.xpos), int(self.ypos)), (int(self.xpos+LINE_LENGTH*self.velocity[0]*math.cos(self.velocity[1])), int(self.ypos+LINE_LENGTH*self.velocity[0]*math.sin(self.velocity[1]))), 1)
    
    def draw(self):
        self.draw_score()
        
        for i in range(0, self.TRAIL+1):
            pygame.draw.circle(screen, ((i*self.rchange), (i*self.gchange),
                               (i*self.bchange)), (int(self.xpoints[i]),
                                                      int(self.ypoints[i])),
                                                          self.size)
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.xpos), int(self.ypos)), self.size)

    def draw_score(self):
        text = font.render((str(self.health)), True, (self.r, self.g, self.b), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (self.initX+self.size, self.initY+self.size)
        screen.blit(text, textRect)

class AI(Player):
    def __init__(self, xpos, ypos, mass, size, init_vect, player):
        self.TRAIL = 8
        self.LIM = 2
        self.SHOOT_V = 3
        self.health = HEALTH

        self.initX = xpos
        self.initY = ypos

        self.xpos = float(xpos)
        self.ypos = float(ypos)
        self.mass = mass
        self.size = size

        self.xpoints = []
        self.ypoints = []

        self.add_time = time.time()+random.uniform(0, 5)
        self.at = 5
        self.add_timeB = time.time()+random.uniform(0, 10)
        self.atB = 10
        self.add_timeC = time.time()+random.uniform(0, 10)
        self.atC = 20
        self.add_timeD = time.time()+random.uniform(0, 10)
        self.atD = 8
        self.add_timeE = time.time()+random.uniform(0, 10)
        self.atE = 35
        self.add_timeF = time.time()+random.uniform(0, 10)
        self.atF = 25
        self.add_timeG = time.time()+random.uniform(0, 10)
        self.atG = 40

        self.player = player

        self.ID = False

        for i in range(0, self.TRAIL+1):
            self.xpoints.append(self.xpos)
            self.ypoints.append(self.ypos)

        self.r = int(random.uniform(100, 225))
        self.g = int(random.uniform(100, 225))
        self.b = int(random.uniform(100, 225))

        self.rchange = (self.r-10)//self.TRAIL
        self.gchange = (self.g-10)//self.TRAIL
        self.bchange = (self.b-10)//self.TRAIL

        self.velocity = init_vect

    def move(self):
        global objects

        self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        self.ypos+=self.velocity[0]*math.sin(self.velocity[1])
        
        if self.health>0:
            if self.xpos>WINDOW_W-self.size:
                self.xpos = WINDOW_W-self.size
            if self.xpos<self.size:
                self.xpos = self.size
            if self.ypos>WINDOW_H-self.size:
                self.ypos = WINDOW_H-self.size
            if self.ypos<self.size:
                self.ypos = self.size
                
            if time.time()-self.add_time>self.at:
                objects.append(Projectile(self.xpos, self.ypos, 10, 5, [self.velocity[0]+self.SHOOT_V, self.velocity[1]], self.player))
                objects[len(objects)-1].move()
                objects[len(objects)-1].move()
                BLAST_SOUND.play()
                self.add_time = time.time()+random.uniform(0, 5)

            if (time.time()-self.add_timeB>self.atB and self.velocity[0]>0.4) and avAb[0]>0:
                objects.append(ProjectileB(self.xpos, self.ypos, 0, 5, [self.velocity[0], self.velocity[1]], self.player))
                objects[len(objects)-1].move()
                if avAb[0]==1:
                    BLAST_SOUND.play()
                self.add_timeB = time.time()+random.uniform(0, 10)

            if time.time()-self.add_timeC>self.atC and avAb[1]>0:
                objects.append(Projectile(self.xpos, self.ypos, 10, 5, [1, self.velocity[1]], self.player))
                objects[len(objects)-1].move()
                if avAb[1]==1:
                    BLAST_SOUND.play()
                self.add_timeC = time.time()+random.uniform(0, 10)

            if time.time()-self.add_timeD>self.atD and avAb[2]>0 and self.velocity[0]>2:
                objects.append(BlackHole(self.xpos, self.ypos, 250, 15, [-10, self.velocity[1]]))
                for i in range(0, 5):
                    objects[len(objects)-1].place_move()
                if avAb[2]==1:
                    BLACK_HOLE_SOUND.play()
                self.add_timeD = time.time()+random.uniform(0, 15)
            if time.time()-self.add_timeE>self.atE and avAb[3]>0 and self.velocity[0]>2:
                objects.append(WhiteHole(self.xpos, self.ypos, 250, 15, [-10, self.velocity[1]]))
                for i in range(0, 5):
                    objects[len(objects)-1].place_move()
                if avAb[3]==1:
                    WHITE_HOLE_SOUND.play()
                self.add_timeE = time.time()+random.uniform(0, 15)

            if time.time()-self.add_timeF>self.atF and avAb[4]>0:
                objects.append(Projectile(self.xpos, self.ypos, 150, 10, [self.velocity[0]+3, self.velocity[1]], self.player))
                objects[len(objects)-1].move()
                objects[len(objects)-1].move()
                objects[len(objects)-1].move()
                objects[len(objects)-1].move()
                objects[len(objects)-1].move()
                if avAb[4]==1:
                    BLAST_SOUND.play()
                self.add_timeF = time.time()+random.uniform(0, 8)

            if time.time()-self.add_timeG>self.atG and avAb[5]>0:
                objects.append(WormHole(self.xpos, self.ypos, 80, 5, [-10, self.velocity[1]]))
                for i in range(0, 5):
                    objects[len(objects)-1].place_move()
                if avAb[5]==1:
                    WORM_HOLE_SOUND.play()
                self.add_timeG = time.time()+random.uniform(0, 10)

        for i in range(0, self.TRAIL):
            self.xpoints[i] = self.xpoints[i+1]
            self.ypoints[i] = self.ypoints[i+1]

        self.xpoints[self.TRAIL] = self.xpos
        self.ypoints[self.TRAIL] = self.ypos

class BlackHole(Planet):
    def __init__(self, xpos, ypos, mass, size, init_vect):
        super().__init__(xpos, ypos, mass, size, init_vect)

        self.r = 60
        self.g = 60
        self.b = 60

        self.player = -1

        self.initX = xpos*-1000
        self.initY = ypos*-1000

    def place_move(self):
        self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        self.ypos+=self.velocity[0]*math.sin(self.velocity[1])
        
class WhiteHole(Planet):
    def __init__(self, xpos, ypos, mass, size, init_vect):
        super().__init__(xpos, ypos, mass, size, init_vect)

        self.r = 255
        self.g = 255
        self.b = 255

        self.player = -2

        self.initX = xpos*-2000
        self.initY = ypos*-2000

    def place_move(self):
        self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        self.ypos+=self.velocity[0]*math.sin(self.velocity[1])

class Void(Planet):
    def __init__(self, xpos, ypos, mass, size, init_vect):
        super().__init__(xpos, ypos, mass, size, init_vect)

        self.initX = xpos*-1500
        self.initY = ypos*-1500

        self.ID = True

        self.uses = 3
    
    def collide(self):
        if self.mass!=0:
            for i in range(0, len(objects)):
                diffX = objects[i].xpos-self.xpos
                diffY = objects[i].ypos-self.ypos

                dist = math.sqrt(pow(diffX, 2)+pow(diffY, 2))

                if (dist<(self.size+objects[i].size+10) and not(objects[i].ID)) and self.uses>0:
                    self.uses-=1
                    objects[i].xpos = random.uniform(100, WINDOW_W-100)
                    objects[i].ypos = random.uniform(100, WINDOW_H-100)
                    objects[i].velocity = [1.0, objects[i].velocity[1]]
                    if avAb[5]==1:
                        APPEAR_SOUND.play()
                    time.sleep(0.25)
                    if self.uses<=0:
                        if avAb[5]==1:
                            CLOSE_SOUND.play()
                elif self.uses<=0:
                    self.xpos=self.initX
                    self.ypos=self.initY

    def place_move(self):
        self.xpos+=self.velocity[0]*math.cos(self.velocity[1])
        self.ypos+=self.velocity[0]*math.sin(self.velocity[1])
                    
    def draw(self):
        pygame.draw.circle(screen, (148, 0, 211), (int(self.xpos), int(self.ypos)), self.size, 1)
        pygame.draw.line(screen, (104, 104, 176), (int(self.xpos+15), int(self.ypos-15)), (int(self.xpos-15), int(self.ypos+15)), 1)
        pygame.draw.line(screen, (104, 104, 176), (int(self.xpos-15), int(self.ypos+15)), (int(self.xpos), int(self.ypos+40)), 1)
        pygame.draw.line(screen, (104, 104, 176), (int(self.xpos+15), int(self.ypos-15)), (int(self.xpos), int(self.ypos-40)), 1)


# Math

class Forces(object):
    
    def gravity(self):
        global objects

        for i in range(0, len(objects)):
            for j in range(i+1, len(objects)):
                if(objects[i].mass!=0 or objects[j].mass!=0):
                    grav(i, j)


def grav(i, j):

    global objects
    global G

    diffX = objects[j].xpos-objects[i].xpos
    diffY = objects[j].ypos-objects[i].ypos

    if diffX==0:
        diffX = 0.00000001

    dist = math.sqrt(pow(diffX, 2)+pow(diffY,2))

    if dist<1:
        dist = 1

    ang = math.atan(diffY/diffX)

    if diffX<0:
        ang+=math.pi

    force = (G*objects[i].mass*objects[j].mass)/(pow(dist, 2))

    if objects[i].player!=-2 and objects[j].player!=-2:
        objects[i].add_velocity(zero_div(force, objects[i].mass), ang)
        objects[j].add_velocity(zero_div(force, objects[j].mass), ang+math.pi)
    else:
        objects[i].add_velocity(zero_div(force, objects[i].mass), ang+math.pi)
        objects[j].add_velocity(zero_div(force, objects[j].mass), ang)

def delete_extra():
    global game_over
    global objects
    global songsAct

    amtlv = 0

    indices = []

    for i in range(0, len(objects)):
        if objects[i].health>0:
            amtlv+=1
        
        if objects[i].isOut():
            objects[i].mass = 0
            indices.append(i)

    indices.reverse()

    if len(indices)>0:
        for i in range(0, len(indices)):
            objects.pop(indices[i])

    if amtlv<=1:
        pi = 0
        
        for i in range(0, len(objects)):
            if objects[i].health>0:
                pi = objects[i].player
                
        WIN_SOUND.play()
        time.sleep(3)

        draw_end(pi)
        print(pi)

        time.sleep(3)
        
        game_over = True

        songsAct = False
        
        pygame.mixer.music.load('GameSounds/spacesound.ogg')

        pygame.mixer.music.play()

def zero_div(n, d):
    return n / d if d else 0

class Stars(object):
    def __init__(self):
        
        self.pos = []

        for i in range(0, NUM_STARS):
            self.pos.append(int(WINDOW_W*random.random()))
            self.pos.append(int(WINDOW_H*random.random()))

    def draw(self):
        
        for i in range(0, 2*NUM_STARS, 2):
            pygame.draw.circle(screen, (255, 255, 255), (self.pos[i], self.pos[i+1]), 1)

stars = Stars()

forces = Forces()

zero_vect = [0.0, 0.0]
test_vect = [0.0, 0.0]

#proj = Projectile(650, 50, 10, 5, test_vect, 1)
p1 = Planet(int(random.uniform(100, 450)), int(random.uniform(100, 375)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p2 = Planet(int(random.uniform(100, 450)), int(random.uniform(375, 650)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p3 = Planet(int(random.uniform(750, 1100)), int(random.uniform(100, 375)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p4 = Planet(int(random.uniform(750, 1100)), int(random.uniform(375, 650)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p5 = Planet(int(random.uniform(450, 750)), int(random.uniform(100, 375)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p6 = Planet(int(random.uniform(450, 750)), int(random.uniform(375, 650)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p7 = Planet(int(random.uniform(100, 1100)), int(random.uniform(100, 375)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p8 = Planet(int(random.uniform(100, 1100)), int(random.uniform(375, 650)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p9 = Planet(int(random.uniform(100, 600)), int(random.uniform(100, 375)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
p10 = Planet(int(random.uniform(600, 1100)), int(random.uniform(375, 650)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)

# Xpos, Ypos, Mass, Radius, Initial Vector, Keys, Player Number

# A=Projectile B=Slow Projectile C=Escape Projectile D=Black Hole E=White Hole F=Heavy Projectile G=Void

player1 = Player(50, 50, 30, 7, zero_vect, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_x, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_r, 1)
player2 = Player(50, WINDOW_H-50, 30, 7, zero_vect, pygame.K_b, pygame.K_m, pygame.K_h, pygame.K_n, pygame.K_g, pygame.K_j, pygame.K_v, pygame.K_k, pygame.K_y, pygame.K_i, pygame.K_t, pygame.K_u, 2)
player3 = Player(WINDOW_W-50, 50, 30, 7, zero_vect, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_p, pygame.K_SEMICOLON, pygame.K_BACKSLASH, pygame.K_PERIOD, pygame.K_QUOTE, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_SLASH,  3)
player4 = Player(WINDOW_W-50, WINDOW_H-50, 30, 7, zero_vect, pygame.K_KP4, pygame.K_KP6, pygame.K_KP8, pygame.K_KP2, pygame.K_KP7, pygame.K_KP9, pygame.K_KP1, pygame.K_KP3, pygame.K_KP5, pygame.K_KP_MULTIPLY, pygame.K_KP_MINUS, pygame.K_KP_DIVIDE, 4)


ai1 = AI(50, 50, 30, 7, zero_vect, 1)
ai2 = AI(50, WINDOW_H-50, 30, 7, zero_vect, 2)
ai3 = AI(WINDOW_W-50, 50, 30, 7, zero_vect, 3)
ai4 = AI(WINDOW_W-50, WINDOW_H-50, 30, 7, zero_vect, 4)


def reset():
    global objects

    objects = []

    stars = Stars()

    forces = Forces()

    zero_vect = [0.0, 0.0]
    test_vect = [0.0, 0.0]

    #proj = Projectile(650, 50, 10, 5, test_vect, 1)
    p1 = Planet(int(random.uniform(100, 450)), int(random.uniform(100, 350)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
    p2 = Planet(int(random.uniform(100, 450)), int(random.uniform(350, 600)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
    p3 = Planet(int(random.uniform(750, 1100)), int(random.uniform(100, 350)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
    p4 = Planet(int(random.uniform(750, 1100)), int(random.uniform(350, 600)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
    p5 = Planet(int(random.uniform(450, 750)), int(random.uniform(100, 350)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)
    p6 = Planet(int(random.uniform(450, 750)), int(random.uniform(350, 600)), int(random.uniform(200, 650)), int(random.uniform(18, 35)), zero_vect)

    # Xpos, Ypos, Mass, Radius, Initial Vector, Keys, Player Number

    player1 = Player(50, 50, 30, 7, zero_vect, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_q, pygame.K_e, pygame.K_z, pygame.K_x, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_r, 1)
    player2 = Player(50, WINDOW_H-50, 30, 7, zero_vect, pygame.K_b, pygame.K_m, pygame.K_h, pygame.K_n, pygame.K_g, pygame.K_j, pygame.K_v, pygame.K_k, pygame.K_y, pygame.K_i, pygame.K_t, pygame.K_u, 2)
    player3 = Player(WINDOW_W-50, 50, 30, 7, zero_vect, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_p, pygame.K_SEMICOLON, pygame.K_BACKSLASH, pygame.K_PERIOD, pygame.K_QUOTE, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_SLASH,  3)
    player4 = Player(WINDOW_W-50, WINDOW_H-50, 30, 7, zero_vect, pygame.K_KP4, pygame.K_KP6, pygame.K_KP8, pygame.K_KP2, pygame.K_KP7, pygame.K_KP9, pygame.K_KP1, pygame.K_KP3, pygame.K_KP5, pygame.K_KP_MULTIPLY, pygame.K_KP_MINUS, pygame.K_KP_DIVIDE, 4)

    ai1 = AI(50, 50, 30, 7, zero_vect, 1)
    ai2 = AI(50, WINDOW_H-50, 30, 7, zero_vect, 2)
    ai3 = AI(WINDOW_W-50, 50, 30, 7, zero_vect, 3)
    ai4 = AI(WINDOW_W-50, WINDOW_H-50, 30, 7, zero_vect, 4)

    if NUMPL>0:
        objects.append(p1)
    if NUMPL>1:
        objects.append(p2)
    if NUMPL>2:
        objects.append(p3)
    if NUMPL>3:
        objects.append(p4)
    if NUMPL>4:
        objects.append(p5)
    if NUMPL>5:
        objects.append(p6)
    if NUMPL>6:
        objects.append(p7)
    if NUMPL>7:
        objects.append(p8)
    if NUMPL>8:
        objects.append(p9)
    if NUMPL>9:
        objects.append(p10)

    if playerNums[0]==1:
        objects.append(player1)
    elif playerNums[0]==2:
        objects.append(ai1)

    if playerNums[1]==1:
        objects.append(player2)
    elif playerNums[1]==2:
        objects.append(ai2)

    if playerNums[2]==1:
        objects.append(player3)
    elif playerNums[2]==2:
        objects.append(ai3)

    if playerNums[3]==1:
        objects.append(player4)
    elif playerNums[3]==2:
        objects.append(ai4)

    if not(songsAct):
        new_song()

def game():
    time.sleep(0.1)

    while game_over==False:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():

            if event.type == SONG_END:
                new_song()

            if event.type == KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_song()

                elif event.key == pygame.K_BACKQUOTE:
                    pygame.mixer.music.rewind()
            
            if event.type == pygame.QUIT:
                break
                running = False

        stars.draw()

        forces.gravity()

        for i in range(0, len(objects)):
            objects[i].bounds()
            objects[i].move()
            objects[i].draw()
            objects[i].collide()

        pygame.display.update()

        delete_extra()

        clock.tick(60)

def draw_vol():
    text = font.render((str(round(pygame.mixer.music.get_volume()*100))), True, (141, 56, 207), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (50, 50)
    screen.blit(text, textRect)

def draw_health():
    text = font.render((str(HEALTH)), True, (38, 252, 167), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (WINDOW_W//2, WINDOW_H-100)
    screen.blit(text, textRect)

def draw_planets():
    text = font.render((str(NUMPL)), True, (38, 252, 167), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (WINDOW_W//2, WINDOW_H//2-225)
    screen.blit(text, textRect)

def draw_end(num):
    screen.fill((0, 0, 0))

    if num>0:
        text = font.render("Player "+str(num)+" won!", True, (255, 255, 255), (0, 0, 0))
    else:
        text = font.render("Tie!", True, (255, 255, 255), (0, 0, 0))


    textRect = text.get_rect()  
    textRect.center = (WINDOW_W//2, WINDOW_H//2)
    screen.blit(text, textRect)

    pygame.display.update()

def draw_avAb():
    if avAb[0]==1:
        text = font.render("B", True, (0, 255, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-80, WINDOW_H//2-300)
        screen.blit(text, textRect)
    elif avAb[0]==2:
        text = font.render("B", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-80, WINDOW_H//2-300)
        screen.blit(text, textRect)
    else:
        text = font.render("B", True, (255, 0, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-80, WINDOW_H//2-300)
        screen.blit(text, textRect)

    if avAb[1]==1:
        text = font.render("C", True, (0, 255, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-50, WINDOW_H//2-300)
        screen.blit(text, textRect)
    elif avAb[1]==2:
        text = font.render("C", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-50, WINDOW_H//2-300)
        screen.blit(text, textRect)
    else:
        text = font.render("C", True, (255, 0, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-50, WINDOW_H//2-300)
        screen.blit(text, textRect)

    if avAb[2]==1:
        text = font.render("D", True, (0, 255, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-20, WINDOW_H//2-300)
        screen.blit(text, textRect)
    elif avAb[2]==2:
        text = font.render("D", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-20, WINDOW_H//2-300)
        screen.blit(text, textRect)
    else:
        text = font.render("D", True, (255, 0, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2-20, WINDOW_H//2-300)
        screen.blit(text, textRect)

    if avAb[3]==1:
        text = font.render("E", True, (0, 255, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+10, WINDOW_H//2-300)
        screen.blit(text, textRect)
    elif avAb[3]==2:
        text = font.render("E", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+10, WINDOW_H//2-300)
        screen.blit(text, textRect)
    else:
        text = font.render("E", True, (255, 0, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+10, WINDOW_H//2-300)
        screen.blit(text, textRect)
    if avAb[4]==1:
        text = font.render("F", True, (0, 255, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+40, WINDOW_H//2-300)
        screen.blit(text, textRect)
    elif avAb[4]==2:
        text = font.render("F", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+40, WINDOW_H//2-300)
        screen.blit(text, textRect)
    else:
        text = font.render("F", True, (255, 0, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+40, WINDOW_H//2-300)
        screen.blit(text, textRect)

    if avAb[5]==1:
        text = font.render("G", True, (0, 255, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+70, WINDOW_H//2-300)
        screen.blit(text, textRect)
    elif avAb[5]==2:
        text = font.render("G", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+70, WINDOW_H//2-300)
        screen.blit(text, textRect)
    else:
        text = font.render("G", True, (255, 0, 0), (0, 0, 0))
        textRect = text.get_rect()  
        textRect.center = (WINDOW_W//2+70, WINDOW_H//2-300)
        screen.blit(text, textRect)

def draw_players():
    if playerNums[0]==1:
        pygame.draw.rect(screen, (0, 255, 0), (WINDOW_W//2-55, WINDOW_H//2+200, 20, 20))
    elif playerNums[0]==2:
        pygame.draw.rect(screen, (0, 0, 255), (WINDOW_W//2-55, WINDOW_H//2+200, 20, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (WINDOW_W//2-55, WINDOW_H//2+200, 20, 20))

    if playerNums[1]==1:
        pygame.draw.rect(screen, (0, 255, 0), (WINDOW_W//2-25, WINDOW_H//2+200, 20, 20))
    elif playerNums[1]==2:
        pygame.draw.rect(screen, (0, 0, 255), (WINDOW_W//2-25, WINDOW_H//2+200, 20, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (WINDOW_W//2-25, WINDOW_H//2+200, 20, 20))

    if playerNums[2]==1:
        pygame.draw.rect(screen, (0, 255, 0), (WINDOW_W//2+5, WINDOW_H//2+200, 20, 20))
    elif playerNums[2]==2:
        pygame.draw.rect(screen, (0, 0, 255), (WINDOW_W//2+5, WINDOW_H//2+200, 20, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (WINDOW_W//2+5, WINDOW_H//2+200, 20, 20))

    if playerNums[3]==1:
        pygame.draw.rect(screen, (0, 255, 0), (WINDOW_W//2+35, WINDOW_H//2+200, 20, 20))
    elif playerNums[3]==2:
        pygame.draw.rect(screen, (0, 0, 255), (WINDOW_W//2+35, WINDOW_H//2+200, 20, 20))
    else:
        pygame.draw.rect(screen, (255, 0, 0), (WINDOW_W//2+35, WINDOW_H//2+200, 20, 20))
    

def draw_logo():
    tfont = pygame.font.SysFont("Arial", 50)
    tfont.set_bold(True)
    text = tfont.render(("ORBITS"), True, (96, 130, 166), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (WINDOW_W//2, WINDOW_H//2)
    screen.blit(text, textRect)
    pygame.draw.circle(screen, (255, 255, 255), (WINDOW_W//2, WINDOW_H//2), 150, 3)

def draw_author():
    tfont = pygame.font.SysFont("Arial", 25)
    tfont.set_bold(True)
    text = tfont.render(("BY MIHIR KONDAPALLI"), True, (96, 130, 166), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (WINDOW_W//2, WINDOW_H//2+330)
    screen.blit(text, textRect)

def draw_p(ang, radius, r, g, b, pos):
    pygame.draw.circle(screen, (r, g, b), (int(WINDOW_W//2+radius*math.cos(ang)), int(WINDOW_H//2+radius*math.sin(ang))), 5)

    intangle = ang

    change = pos*0.01

    c_change = 255//20

    

    for i in range(0, 20):
        intangle+=change

        r = less_to_zero(r-c_change)
        g = less_to_zero(g-c_change)
        b = less_to_zero(b-c_change)
        
        pygame.draw.circle(screen, (r, g, b), (int(WINDOW_W//2+radius*math.cos(intangle)), int(WINDOW_H//2+radius*math.sin(intangle))), 1)

def less_to_zero(num):
    if num<0:
        return 0
    return num

def define_health():
    for i in range(0, len(objects)):
        objects[i].health = HEALTH

def adjust_sound_vol(vol):
    BLAST_SOUND.set_volume(vol)
    EXPLO_SOUND.set_volume(vol)
    BLACK_HOLE_SOUND.set_volume(vol)
    WHITE_HOLE_SOUND.set_volume(vol)
    WORM_HOLE_SOUND.set_volume(vol)
    APPEAR_SOUND.set_volume(vol)
    RADAR_SOUND.set_volume(vol)
    CLOSE_SOUND.set_volume(vol)
    WIN_SOUND.set_volume(vol)
    CLICK_SOUND.set_volume(vol)


def draw_soundVol():
    shade = int(255*EXPLO_SOUND.get_volume())
    
    text = font.render(str(round(EXPLO_SOUND.get_volume()*100)), True, (shade, shade, shade), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (WINDOW_W-50, 50)
    screen.blit(text, textRect)

def main():
    global HEALTH
    global game_over
    global sound
    global NUMPL
    global songsAct

    pygame.mixer.music.load('GameSounds/spacesound.ogg')

    pygame.mixer.music.play()

    pygame.mixer.music.set_volume(0.5)

    ang1 = 0.0
    ang2 = 0.0

    SPROT = 17

    adjust_sound_vol(0.5)
    
    while True:
        screen.fill((0, 0, 0))
        
        draw_vol()
        draw_health()
        draw_logo()
        draw_author()
        draw_players()
        draw_avAb()
        draw_soundVol()
        draw_planets()

        draw_p(ang1, 350, 255, 0, 0, 1)
        draw_p(ang2, 250, 0, 0, 255, -1)

        ang1-=math.pi/(30*SPROT)
        ang2+=math.pi/(30*SPROT)
        
        pygame.display.update()
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                CLICK_SOUND.play()
                
                if event.key == pygame.K_q:
                    pygame.display.quit()
                    pygame.quit()
                
                if event.key == pygame.K_UP:
                    vol = pygame.mixer.music.get_volume()+0.01

                    if vol>1.0:
                        vol=1.0
                    
                    pygame.mixer.music.set_volume(vol)
                    
                elif event.key == pygame.K_DOWN:
                    vol = pygame.mixer.music.get_volume()-0.01

                    if vol<0.0:
                        vol=0.0
                        
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_RIGHT:
                    HEALTH+=1

                    if HEALTH>25:
                        HEALTH = 25
                        
                    define_health()
                    
                elif event.key == pygame.K_LEFT:
                    HEALTH-=1

                    if HEALTH<1:
                        HEALTH = 1
                        
                    define_health()

                elif event.key == pygame.K_1:
                    playerNums[0] = (playerNums[0]+1)%3

                elif event.key == pygame.K_2:
                    playerNums[1] = (playerNums[1]+1)%3
                    
                elif event.key == pygame.K_3:
                    playerNums[2] = (playerNums[2]+1)%3

                elif event.key == pygame.K_4:
                    playerNums[3] = (playerNums[3]+1)%3

                elif event.key == pygame.K_b:
                    avAb[0] = (avAb[0]+1)%3

                elif event.key == pygame.K_c:
                    avAb[1] = (avAb[1]+1)%3

                elif event.key == pygame.K_d:
                    avAb[2] = (avAb[2]+1)%3

                elif event.key == pygame.K_e:
                    avAb[3] = (avAb[3]+1)%3

                elif event.key == pygame.K_f:
                    avAb[4] = (avAb[4]+1)%3

                elif event.key == pygame.K_g:
                    avAb[5] = (avAb[5]+1)%3
                    
                elif event.key == pygame.K_p:
                    time.sleep(0.1)
                    new_song()
                    songsAct = True

                elif event.key == pygame.K_o:
                    time.sleep(0.1)
                    pygame.mixer.music.load('GameSounds/spacesound.ogg')
                    pygame.mixer.play()
                    
                elif event.key == pygame.K_SPACE:
                    new_song()

                elif event.key == pygame.K_EQUALS:
                    vol = EXPLO_SOUND.get_volume()+0.01

                    if vol>1.0:
                        vol=1.0

                    adjust_sound_vol(vol)

                elif event.key == pygame.K_MINUS:
                    vol = EXPLO_SOUND.get_volume()-0.01

                    if vol<0.0:
                        vol=0.0

                    adjust_sound_vol(vol)

                elif event.key == pygame.K_9:
                    NUMPL-=1
                    if NUMPL<0:
                        NUMPL=0

                elif event.key == pygame.K_0:
                    NUMPL+=1
                    if NUMPL>10:
                        NUMPL=10

                elif event.key == pygame.K_r:
                    pygame.mixer.music.rewind()
                    
                elif event.key == pygame.K_RETURN:
                    game_over = False
                    reset()
                    game()
                
            if event.type == pygame.QUIT:
                break


main()
