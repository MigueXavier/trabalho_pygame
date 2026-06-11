import pygame
import copy
from sys import exit
from src.configuracao import *


class Bloco:
    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)

    def checar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
    
    def clonar_bloco(self):
         return copy.deepcopy(self)


class BlocoDireita(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (0, 200, 0))
        self.tipo = "direita"
        self.clicado = False

    def acao(self):
        if not self.clicado:
         self.clicado = True
         self.cor = (0, 100, 0)


class BlocoEsquerda(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (200, 0, 0))
        self.tipo = "esquerda"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = (100, 0, 0)
class BlocoCima(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (200, 0, 200))
        self.tipo = "cima"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = (100, 0, 100)
class BlocoBaixo(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (0, 200, 200))
        self.tipo = "baixo"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = (0, 100, 100)
















