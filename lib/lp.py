#!/usr/bin/python
import pygame
import sys
from pygame.locals import *
pygame.init
import level
WHITE = (200, 200, 200)
firstlevel = level.Level("test.lvl")
DISPWIDTH = firstlevel.right_edge
DISPHEIGHT = firstlevel.bottom_edge
DISPSURF = pygame.display.set_mode((DISPWIDTH, DISPHEIGHT))
pygame.display.set_caption("level viewer")
firstlevel.load_map("../assets/blocks/")
while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  DISPSURF.fill(WHITE)
  firstlevel.level_group.draw(DISPSURF)
  pygame.display.update()
  pygame.display.flip()
