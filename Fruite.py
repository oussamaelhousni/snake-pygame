import random
from pygame.math import Vector2
import pygame
class Fruit:
    def __init__(self, cell_size,cell_number, screen):
        self.x = 5 * cell_size
        self.y = 4 *  cell_size
        self.cell_size = cell_size
        self.screen = screen
        self.pos = Vector2(self.x, self.y)

    def draw(self, cell_size):
        # create a rectangle
        fruit_rect = pygame.Rect(self.pos.x,self.pos.y,cell_size,cell_size)
        pygame.draw.rect(self.screen, (255,0,0),fruit_rect)
        # draw the rectangle
