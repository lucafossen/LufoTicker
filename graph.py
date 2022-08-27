import pygame

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def draw(self):
        pygame.draw.circle(screen, (255, 200, 0), (self.x, self.y), 3)
