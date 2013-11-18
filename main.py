#!/usr/bin/python
##########################
#Name:  main.py
#Author:  Billy Jackson
#Purpose:  Main pygame loop for police turtle bob prototype
#Date:  11/13/13
##########################
import pygame, sys
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
imgarr.append(pygame.transform.flip(imgarr[0], True, False))
imgarr.append(pygame.transform.flip(imgarr[1], True, False))
bobdelay = 0
bobx = 100
boby = 100

#Build a player class to control ptb as we play.
class player(object):
  def __init__(self, imgarr, startx, starty):
#    pygame.sprite.Sprite().__init__(self)
    self.imgarr = imgarr
    self.x = startx
    self.y = starty
  BOBSPEED = 4
  BOBLIMIT = 3
  bobsurf = imgarr[1]
  bobdelay = 0
  def update(self):
    if keyPressed(K_RIGHT):
      self.x += BOBSPEED
      if bobsurf != imgarr[1] and bobdelay > BOBLIMIT:
        self.bobdelay = 0
        self.bobsurf = imgarr[1]
      if bobsurf != imgarr[0] and bobdelay > BOBLIMIT:
        self.bobdelay = 0
        self.bobsurf = imgarr[0]
      self.bobdelay += 1

def keyPressed(key):
  keysPressed = pygame.key.get_pressed()
  if keysPressed[key]:
    return True
  else:
    return False 
  
while True:
  for event in pygame.event.get():
    if event.type == QUIT or keyPressed(K_ESCAPE):
      pygame.quit()
      sys.exit()
  ptb = player(imgarr, 100, 100)
  DISPSURF.fill(WHITE)
  DISPSURF.blit(ptb.bobsurf, (ptb.x, ptb.y))
  pygame.display.update()
  pygame.display.flip()
  FPSCLOCK.tick(FPS)
  
