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

#################
#Load some sprite images
#################
imgarr = []
imgarr.append(pygame.image.load("assets/bobstand.png").convert_alpha())
imgarr.append(pygame.image.load("assets/bobwalk.png").convert_alpha())

brownblock = pygame.image.load("assets/brownblock.png") 
#################

##################################################
#Build a block class to create something for bob and company
#to stand on.
##################################################
class platform(pygame.sprite.Sprite):
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
    self.future_rect = self.rect.copy()

  revarr = []
  for frame in imgarr:
    revarr.append(pygame.transform.flip(frame, True, False))
  
  JUMPACCEL = -15
  FALLACCEL = 2 
  XACCEL = 2 
  dy = 0
  dx = 0 
  MAXSPEED = 10 
  STANDING = False 

  t1 = time.time()
  MAXFRAMES = len(imgarr)
  FRAMEFLIP = .1
  FRAME = 0

  def platform_collide(self):
    result = self.future_rect.collidelist(levelrect)
    if self.dx > 0 and result > -1:
      self.rect.right = levelrect[result].left - 1
      self.dx = 0
    elif self.dx < 0 and result > -1:
      self.rect.left= levelrect[result].right + 1
      self.dx = 0
    if self.dy > 0 and self.STANDING == False:
      self.rect.bottom = levelrect[result].bottom - 1
      self.STANDING = True
      self.dy = 0

  def update(self):
    #Reset the future rect.
    self.future_rect = self.rect.copy()

    #Compare time and increment the sprite array for animation
    t2 = time.time()
    if t2 - self.t1 > self.FRAMEFLIP:
      self.t1 = time.time()
      if (self.FRAME + 1) == self.MAXFRAMES:
        self.FRAME = 0
      else:
        self.FRAME += 1

    if keyPressed(K_d) and (not keyPressed(K_a)):
      self.image = self.imgarr[self.FRAME]
      if abs(self.dx + self.XACCEL) > self.MAXSPEED:
        self.dx = self.MAXSPEED
      else:
        self.dx += self.XACCEL
      self.future_rect.x += self.dx
      self.platform_collide()
      self.rect.x += self.dx
 
    #Accel left
    if keyPressed(K_a) and (not keyPressed(K_d)):
      self.image = self.revarr[self.FRAME] 
      if abs(self.dx - self.XACCEL) > self.MAXSPEED:
        self.dx = -self.MAXSPEED
      else:
        self.dx -= self.XACCEL
      self.future_rect.x += self.dx
      self.platform_collide()
      self.rect.x += self.dx

    #Stop the darn turtle if no keys are pressed.  We could change this to 
    # decel if we wanted too.
    if not (keyPressed(K_a) or keyPressed(K_d)):  
      self.dx = 0

    #Jump
    if keyPressed(K_w) and self.STANDING:
      self.dy += self.JUMPACCEL
      self.future_rect.y += self.dy
      self.platform_collide()
      self.rect.y += self.dy
 
    #Fall
    #if not self.STANDING:
    #  self.dy += self.FALLACCEL
    #  self.future_rect.y += self.dy
    #  self.platform_collide()
    #  self.rect.y += self.dy
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
ptb = player(imgarr, 400, 100) 
allsprites.add(ptb)

#Instantiate some blocks durnit!
level = pygame.sprite.Group()
levelmap = [] 
levelrect = []
for i in range(0, 800, 32):
  levelmap.append(platform(brownblock, i, 300))
  levelrect.append(platform(brownblock, i, 300).rect)
  if i > 400:  
    levelmap.append(platform(brownblock, i, 250))
    levelrect.append(platform(brownblock, i, 250).rect)

for i in range(0, 400, 32):
  levelmap.append(platform(brownblock, 600, i))
  levelmap.append(platform(brownblock, 300, i))
  levelrect.append(platform(brownblock, 600, i).rect)
  levelrect.append(platform(brownblock, 300, i).rect)

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
