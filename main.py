#!/usr/bin/python
##########################
#Name:  main.py
#Author:  Billy Jackson
#Purpose:  Main pygame loop for police turtle bob prototype
#Date:  11/13/13
##########################
import pygame, sys, time
from pygame.locals import *

FPS = 30
FPSCLOCK = pygame.time.Clock()
DISPWIDTH = 800
DISPHEIGHT = 400
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

pygame.init

DISPSURF = pygame.display.set_mode((DISPWIDTH, DISPHEIGHT))
pygame.display.set_caption("PTB Prototype")

imgarr = []
imgarr.append(pygame.image.load("assets/bobstand.png").convert_alpha())
imgarr.append(pygame.image.load("assets/bobwalk.png").convert_alpha())
 
brownblock = pygame.image.load("assets/brownblock.png") 

##################################################
#Build a block class to create something for bob and company
#to stand on.
##################################################
class block(pygame.sprite.Sprite):
  def __init__(self, img, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = img 
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
##################################################

##################################################
#Build a player class to control ptb as we play.
##################################################
class player(pygame.sprite.Sprite):

  def __init__(self, imgarr, startx, starty):
    pygame.sprite.Sprite.__init__(self)
    self.image = imgarr[0]
    self.rect = self.image.get_rect()
    self.imgarr = imgarr
    self.rect.x = startx
    self.rect.y = starty

  revarr = []
  for frame in imgarr:
    revarr.append(pygame.transform.flip(frame, True, False))
  
  JUMPACCEL = -40
  FALLACCEL = 4
  YSPEED = 0
  XSPEED = 0 

  def canjump(self):
    if self.rect.y > 267:
      return True
    else:
      return False  

  BOBSPEED = 5 
  t1 = time.time()
  MAXFRAMES = len(imgarr)
  i = 0
  def update(self):
    t2 = time.time()
    if t2 - self.t1 > .5:
      if (self.i + 1) == self.MAXFRAMES:
        self.i = 0
      else:
        self.i += 1
    if keyPressed(K_d):
      self.rect.x += self.BOBSPEED
      self.image = self.imgarr[self.i]
    if keyPressed(K_a):
      self.rect.x -= self.BOBSPEED
      self.image = self.revarr[self.i]
    if keyPressed(K_w) and self.canjump():
      self.YSPEED += self.JUMPACCEL
      self.rect.y += self.YSPEED
    if self.rect.y <= 268:
      self.YSPEED += self.FALLACCEL
      if (self.rect.y + self.YSPEED) > 268:
        self.rect.y = 268 
        self.YSPEED = 0
      else:
        self.rect.y += self.YSPEED
################################################

################################################
#Simple utility function to get if a key has been pressed on the keyboard
################################################
def keyPressed(key):
  keysPressed = pygame.key.get_pressed()
  if keysPressed[key]:
    return True
  else:
    return False 
################################################
#Create an all sprites list
allsprites = pygame.sprite.Group()

#Instantiate bob and start the main game loop 
ptb = player(imgarr, 100, 268) 
ptb.JUMPACCEL = -50
allsprites.add(ptb)

#Instantiate some blocks durnit!
level = pygame.sprite.Group()
levelmap = [] 
for i in range(0, 800, 32):
  levelmap.append(block(brownblock, i, 300))

level.add(levelmap)  
allsprites.add(levelmap)

while True:
  for event in pygame.event.get():
    if event.type == QUIT or keyPressed(K_ESCAPE):
      pygame.quit()
      sys.exit()
  ptb.update()
  DISPSURF.fill(WHITE)
  allsprites.draw(DISPSURF)
  pygame.display.update()
  pygame.display.flip()
  FPSCLOCK.tick(FPS)
  
