import pygame

class Item:
    def desenhar(self, superficie, x, y):
        pygame.draw.circle(
            superficie,
            (255, 255, 0),
            (x + 25, y + 25),
            10
        )