import pygame


class CentralLocation:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    @staticmethod
    def rect_border_color():
        return 0, 0, 0

    def draw(self, screen):
        rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(screen, self.rect_border_color(), rectangle, 2)
