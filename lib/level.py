#!/usr/bin/python
import os
import pygame
import platform
class Level(object):
  block_height = 32
  block_width = 32
  def __init__(self):
    self.tile_width = 0
    self.tile_height = 0 
    self.left_edge = 0
    self.rigth_edge = 0
    self.right_edge = 0
    self.bottom_edge = 0
    self.level_group = pygame.sprite.Group()
    self.levelmap = []
    self.block_dict = {}

  def load_file(self, file):
    self.text = [row.strip('\n') for row in\
                 open(file, 'r').readlines()]
    for line in self.text:
      if len(line) > self.tile_width:
        self.tile_width = len(line)
      self.tile_height = len(self.text)
      self.right_edge = self.tile_width * self.block_width
      self.bottom_edge = self.tile_height * self.block_height

  def load_blocks(self, block_dir):
    for file in os.listdir(block_dir):
      surface = pygame.image.load(block_dir + "/" + file).convert_alpha()
      self.block_dict.update({file: surface})
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
