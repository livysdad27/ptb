#!/usr/bin/python
import os
import pygame
import platform
class Level(object):
  block_height = 32
  block_width = 32
  block_dict = {}
  block_dir = "../assets/blocks/"
  for file in os.listdir(block_dir):
    surface = pygame.image.load(block_dir + file)
    block_dict.update({file: surface}) 
  def __init__(self, file):
    self.text = [row.strip('\n') for row in\
                     open(file, 'r').readlines()]
    self.tile_width = len(self.text[0])
    self.tile_height = len(self.text) 
    self.left_edge = 0
    self.rigth_edge = 0
    self.right_edge = self.tile_width * self.block_width
    self.bottom_edge = self.tile_height * self.block_height
    self.level_group = pygame.sprite.Group()
    self.levelmap = []
    y_coord = 0
    for row in self.text:
      x_coord = 0
      for letter in row:
        if letter != ' ':
          self.levelmap.append(platform.Platform(self.block_dict[letter], x_coord, y_coord))
        x_coord += self.block_width 
      y_coord += self.block_height 
    self.levelrect = [p.rect for p in self.levelmap]
    self.level_group.add(self.levelmap)
