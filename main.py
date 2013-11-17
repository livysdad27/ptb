#!/usr/bin/python
##########################
#Name:  main.py
#Author:  Billy Jackson
#Purpose:  Main pygame loop for police turtle bob prototype
#Date:  11/13/13
##########################
#$Id: main.py,v 1.2 2013/11/17 18:00:48 billylee Exp billylee $
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
bobsurf = imgarr[0]
bobdelay = 0
bobx = 100
boby = 100

def bobanim(imgarr, direction, bobdelay ,x, y, bobsurf):
  BOBLIMIT = 3 
  BOBSPEED = 1 
  if direction == "right":
    x += BOBSPEED 
    if bobsurf != imgarr[1] and bobdelay > BOBLIMIT:
      bobdelay = 0
      bobsurf = imgarr[1]
    if bobsurf != imgarr[0] and bobdelay > BOBLIMIT:
      bobdelay = 0
      bobsurf = imgarr[0]
  if direction == "left":
    x -= BOBSPEED 
    if bobsurf != imgarr[3] and bobdelay > BOBLIMIT:
      bobdelay = 0
      bobsurf = imgarr[3] 
    if bobsurf != imgarr[2] and bobdelay > BOBLIMIT:
      bobdelay = 0 
      bobsurf = imgarr[2] 
  bobdelay += 1
  return x, y, bobsurf, bobdelay 

def keyPressed(key):
  keysPressed = pygame.key.get_pressed()
  if keysPressed[key]:
    return True
  else:
    return False 
  
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  if keyPressed(K_d): 
    bobx, boby, bobsurf, bobdelay = bobanim(imgarr, "right", bobdelay, bobx, boby, bobsurf)
  elif keyPressed(K_a):  
    bobx, boby, bobsurf, bobdelay = bobanim(imgarr, "left", bobdelay, bobx, boby, bobsurf)

  DISPSURF.fill(WHITE)
  DISPSURF.blit(bobsurf, (bobx, boby))
  pygame.display.update()
  FPSCLOCK.tick(FPS)
  
