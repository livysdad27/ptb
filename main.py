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
    self.future_rect = self.rect

  revarr = []
  for frame in imgarr:
    revarr.append(pygame.transform.flip(frame, True, False))
  
  JUMPACCEL = -15
  FALLACCEL = 2 
  XACCEL = 2 
  dy = 0
  dx = 0 
  MAXSPEED = 10 

#  def getCollide(self):
#    blocklist = pygame.sprite.spritecollide(self, level, False)
#    for block in blocklist:
#      print str(self.rect.right) + ":" + str(block.rect.left)
#      if self.rect.top <= block.rect.bottom:  print "hit my head!!!"
#      if self.rect.bottom >= block.rect.top:  print "hit my feet!!!"
#      if self.rect.right >= block.rect.left:  print "hit my right side!!!"
#      if self.rect.left <= block.rect.right:  print "hit my left side!!!"
        
  t1 = time.time()
  MAXFRAMES = len(imgarr)
  FRAMEFLIP = .1
  FRAME = 0

  def is_standing(self):
    if pygame.sprite.spritecollide(self, level, False):
      for block in pygame.sprite.spritecollide(self, level, False):
        if block.rect.top <= self.rect.bottom:
          self.rect.bottom = block.rect.top + 1
          self.dy = 0
          return True
    else:
      return False

  def update(self):
    #Compare time and increment the sprite array
    t2 = time.time()
    if t2 - self.t1 > self.FRAMEFLIP:
      self.t1 = time.time()
      if (self.FRAME + 1) == self.MAXFRAMES:
        self.FRAME = 0
      else:
        self.FRAME += 1

    #See if we're standing
    STANDING = self.is_standing()
 
    if keyPressed(K_d) and (not keyPressed(K_a)):
      self.image = self.imgarr[self.FRAME]
      if abs(self.dx + self.XACCEL) > self.MAXSPEED:
        self.dx = self.MAXSPEED
      else:
        self.dx += self.XACCEL
      self.rect.x += self.dx
 
    #Accel left
    if keyPressed(K_a) and (not keyPressed(K_d)):
      self.image = self.revarr[self.FRAME] 
      if abs(self.dx - self.XACCEL) > self.MAXSPEED:
        self.dx = -self.MAXSPEED
      else:
        self.dx -= self.XACCEL
      self.rect.x += self.dx

    #Stop the darn turtle if no keys are pressed.  We could change this to 
    # decel if we wanted too.
    if not (keyPressed(K_a) or keyPressed(K_d)):  
      self.dx = 0

    #Jump
    if keyPressed(K_w) and STANDING:
      self.dy += self.JUMPACCEL
      self.rect.y += self.dy
 
    #Fall
    if not STANDING:
      self.dy += self.FALLACCEL
      self.rect.y += self.dy
    print self.dy
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
ptb = player(imgarr, 100, 200) 
allsprites.add(ptb)

#Instantiate some blocks durnit!
level = pygame.sprite.Group()
levelmap = [] 
levelrect = []
for i in range(0, 800, 32):
  levelmap.append(platform(brownblock, i, 300))
  levelrect.append(platform(brownblock, i, 300).rect)
  if i > 400:  levelmap.append(platform(brownblock, i, 250))

for i in range(0, 400, 32):
  levelmap.append(platform(brownblock, 600, i))

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
