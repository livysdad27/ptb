#!/usr/bin/python
import pygame
class Platform(pygame.sprite.Sprite):
  def __init__(self, img, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = img
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.top_rect = pygame.Rect(self.rect.left, \
                    self.rect.top, self.rect.width, 1)
    self.bottom_rect = pygame.Rect(self.rect.left, \
                    self.rect.bottom, self.rect.width, 1)
    self.left_rect = pygame.Rect(self.rect.left, \
                     self.rect.top, 1, self.rect.height)
    self.right_rect = pygame.Rect(self.rect.right, \
                     self.rect.top, 1, self.rect.height)

