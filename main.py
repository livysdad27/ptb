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

#################################################
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
    self.top_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 1)
    self.bottom_rect = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width, 1)
    self.left_rect = pygame.Rect(self.rect.left, self.rect.top, 1, self.rect.height)
    self.right_rect = pygame.Rect(self.rect.right, self.rect.top, 1, self.rect.height)
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
  
  JUMPACCEL = -16
  FALLACCEL = 2 
  XACCEL = 2 
  dy = 0
  dx = 0 
  MAXSPEED = 3 
  STANDING = False 

  t1 = time.time()
  MAXFRAMES = len(imgarr)
  FRAMEFLIP = .1
  FRAME = 0

  #Method to test if we collide with a platform
  def platform_collide(self):
    result = self.future_rect.collidelist(levelrect)
    collision_dict = {"left": False, "right": False, "top": False, "bottom": False} 
    ##############
    #Determine which parts of a platform block we've hit
    ##############
    if self.future_rect.colliderect(levelmap[result].left_rect):
      collision_dict["left"] = True
    if self.future_rect.colliderect(levelmap[result].right_rect):
      collision_dict["right"] = True 
    if self.future_rect.colliderect(levelmap[result].top_rect):
      collision_dict["top"] = True 
    if self.future_rect.colliderect(levelmap[result].bottom_rect):
      collision_dict["bottom"] = True
    return collision_dict, levelmap[result]

  def is_standing(self):
   self.future_rect.y += self.dy + self.FALLACCEL
   collision_dict, block = self.platform_collide()
   self.future_rect.y = self.rect.y
   if collision_dict["top"] == 1:
     self.rect.bottom = block.rect.top -1
     self.dy = 0
     return True
   else:
     return False

  def update(self):
    #Reset the future rect determine standing status
    self.future_rect = self.rect.copy()
    self.STANDING = self.is_standing() 

    #Compare time and increment the sprite array for animation
    t2 = time.time()
    if t2 - self.t1 > self.FRAMEFLIP:
      self.t1 = time.time()
      if (self.FRAME + 1) == self.MAXFRAMES:
        self.FRAME = 0
      else:
        self.FRAME += 1
    
    if keyPressed(K_d) and keyPressed(K_a):
      dx = 0

    if keyPressed(K_d) and (not keyPressed(K_a)):
      self.image = self.imgarr[self.FRAME]
      if abs(self.dx + self.XACCEL) > self.MAXSPEED:
        self.dx = self.MAXSPEED
      else:
        self.dx += self.XACCEL
      self.future_rect.x += self.dx
      collision_dict, block_hit = self.platform_collide()
      if collision_dict["left"]:
        self.rect.right = block_hit.rect.left - 1
        self.dx = 0
      else:
        self.rect.x += self.dx
 
    #Accel left
    if keyPressed(K_a) and (not keyPressed(K_d)):
      self.image = self.revarr[self.FRAME] 
      if abs(self.dx - self.XACCEL) > self.MAXSPEED:
        self.dx = -self.MAXSPEED
      else:
        self.dx -= self.XACCEL
      self.future_rect.x += self.dx
      collision_dict, block_hit = self.platform_collide()
      if collision_dict["right"]:
        self.rect.left = block_hit.rect.right + 1
        self.dx = 0
      else: 
        self.rect.x += self.dx

    #Stop the darn turtle if no keys are pressed.  We could change this to 
    # decel if we wanted too.
    if not (keyPressed(K_a) or keyPressed(K_d)):  
      self.dx = 0
    
    #Jump
    if keyPressed(K_w) and self.STANDING:
      self.dy += self.JUMPACCEL
      self.future_rect.y += self.dy
      collision_dict, block_hit = self.platform_collide()
      if collision_dict["bottom"] and not (collision_dict["left"] or collision_dict["right"]):
        self.rect.top = block_hit.rect.bottom +1
        self.dy = 0
      else:
        self.rect.y += self.dy
 
    #Fall
    if not self.STANDING:
      self.dy += self.FALLACCEL
      if self.dy < 0:
        self.future_rect.y += self.dy
        collision_dict, block_hit = self.platform_collide()
        if collision_dict["bottom"]:
          self.rect.top = block_hit.rect.bottom + 1
          self.dy = 0
      self.rect.y += self.dy

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
for i in range(0, 800, 32):
  levelmap.append(platform(brownblock, i, 300))
  if i > 400:  
    levelmap.append(platform(brownblock, i, 200))

for i in range(0, 400, 32):
  levelmap.append(platform(brownblock, 600, i))
  levelmap.append(platform(brownblock, 300, i))

levelrect = [p.rect for p in levelmap]

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
