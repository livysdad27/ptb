#!/usr/bin/python
import pygame
import sys
import time
from pygame.locals import *
pygame.init
from lib import level

level_dir = "./levels/"
block_dir = "./assets/blocks/"
WHITE = (200, 200, 200)
FLASH_COLOR = (20, 200, 200)
EDIT_MODE = False
BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32
FLASH_FREQ = .4
editlevel = level.Level()
t1 = time.time()

if len(sys.argv) < 2:
  print "Usage is le.py <file_name> or le.py width height <file_name>"
  sys.exit()

if len(sys.argv) < 3:
  level_file  = sys.argv[1]
  EDIT_MODE = True

if len(sys.argv) > 3:
  level_file = sys.argv[3]
  level_width = sys.argv[1]
  level_height = sys.argv[2]
  EDIT_MODE = False
    
if EDIT_MODE == True:
  editlevel.load_file(level_dir + level_file)
  DISPWIDTH = editlevel.right_edge
  DISPHEIGHT = editlevel.bottom_edge
else:
  DISPWIDTH = int(level_width) * BLOCK_WIDTH
  DISPHEIGHT= int(level_height) * BLOCK_HEIGHT
  

DISPSURF = pygame.display.set_mode((DISPWIDTH, DISPHEIGHT))
pygame.display.set_caption("level viewer")
editlevel.load_blocks(block_dir)

cursor_rect = pygame.rect.Rect(0, 0, BLOCK_WIDTH, BLOCK_HEIGHT)

while True:
  t2 = time.time()
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  DISPSURF.fill(WHITE)
  editlevel.level_group.draw(DISPSURF)
  if (t2 - t1) > FLASH_FREQ:
    DISPSURF.fill(FLASH_COLOR, cursor_rect) 
    if (t2 - t1) > (2 * FLASH_FREQ):
      t1 = time.time() 
  pygame.display.update()
  pygame.display.flip()
