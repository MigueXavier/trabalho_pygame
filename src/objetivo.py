import pygame
import sys


class Objetivo:
    def __init__(self,  largura_altura, color):
        self.x = None
        self.y = None
        self.width = largura_altura
        self.height = largura_altura
        self.color = color
    
    def desenhar(self, superficie, x, y):
        pygame.draw.rect(superficie, self.color, (x + 15, y, self.width, self.height))