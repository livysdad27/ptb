#!/usr/bin/python
import pygame
import sys
from pygame.locals import *
pygame.init
from lib import level

level_dir = "./levels/"

if len(sys.argv) > 1:
  level_file = sys.argv[1]
else:
  print "specify a level name please!"
  sys.exit()

if len(sys.argv) > 2:
  block_dir = sys.argv[2]
else:
  block_dir = "./assets/blocks"
    
WHITE = (200, 200, 200)
firstlevel = level.Level()
firstlevel.load_file(level_dir + level_file)
DISPWIDTH = firstlevel.right_edge
DISPHEIGHT = firstlevel.bottom_edge
DISPSURF = pygame.display.set_mode((DISPWIDTH, DISPHEIGHT))
pygame.display.set_caption("level viewer")
firstlevel.load_blocks(block_dir)
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  DISPSURF.fill(WHITE)
  firstlevel.level_group.draw(DISPSURF)
  pygame.display.update()
  pygame.display.flip()
