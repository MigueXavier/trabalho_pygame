import pygame
import sys
from src.configuracao import *



class Barreira:
    def __init__(self, largura_altura, color):
        self.x = None
        self.y = None
        self.width = largura_altura
        self.height = largura_altura
        self.color = color
        self.sprite = pygame.image.load("assets/sprites/sprits-jogo-python/obstaculo.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (TAMANHO_CELULA, TAMANHO_CELULA))

    def desenhar(self, superficie, x, y):
        rect = self.sprite.get_rect(topleft=(x, y))
        superficie.blit(self.sprite, rect)
    

