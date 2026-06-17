import pygame
import sys
from src.configuracao import *


class Objetivo:
    def __init__(self):
        self.x = None
        self.y = None
        self.sprite = pygame.image.load("assets/sprites/sprits-jogo-python/estrela.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (TAMANHO_CELULA -20 , TAMANHO_CELULA -20))
    
    def desenhar(self, superficie, x, y):
        rect = self.sprite.get_rect(center=(x + 25, y + 25))
        superficie.blit(self.sprite, rect)