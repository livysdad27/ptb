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

pygame.init

DISPSURF = pygame.display.set_mode((DISPWIDTH, DISPHEIGHT))
pygame.display.set_caption("PTB Prototype")

imgarr = []
imgarr.append(pygame.image.load("assets/bobstand.png").convert_alpha())
imgarr.append(pygame.image.load("assets/bobwalk.png").convert_alpha())

##################################################
#Build a player class to control ptb as we play.
class player(pygame.sprite.Sprite):

  def __init__(self, imgarr, startx, starty):
    pygame.sprite.Sprite().__init__()
    self.image = imgarr[0]
    self.rect = self.image.get_rect()
    self.imgarr = imgarr
    self.x = startx
    self.y = starty

  revarr = []
  for frame in imgarr:
    revarr.append(pygame.transform.flip(frame, True, False))
  
  JUMPACCEL = -40
  FALLACCEL = 4
  YSPEED = 0
  XSPEED = 0 

  def canjump(self):
    if self.y > 299:
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
      self.x += self.BOBSPEED
      self.image = self.imgarr[self.i]
    if keyPressed(K_a):
      self.x -= self.BOBSPEED
      self.image = self.revarr[self.i]
    if keyPressed(K_w) and self.canjump():
      self.YSPEED += self.JUMPACCEL
      self.y += self.YSPEED
    if self.y <= 300:
      self.YSPEED += self.FALLACCEL
      if (self.y + self.YSPEED) > 300:
        self.y = 300
        self.YSPEED = 0
      else:
        self.y += self.YSPEED
################################################
################################################
#Simple utility function to get if a key has been pressed on the keyboard
def keyPressed(key):
  keysPressed = pygame.key.get_pressed()
  if keysPressed[key]:
    return True
  else:
    return False 
################################################

#Instantiate bob and start the main game loop 
ptb = player(imgarr, 100, 300) 
ptb.JUMPACCEL = -20
while True:
  for event in pygame.event.get():
    if event.type == QUIT or keyPressed(K_ESCAPE):
      pygame.quit()
      sys.exit()
  ptb.update()
  DISPSURF.fill(WHITE)
  DISPSURF.blit(ptb.image, (ptb.x, ptb.y))
  pygame.display.update()
  pygame.display.flip()
  FPSCLOCK.tick(FPS)
  
