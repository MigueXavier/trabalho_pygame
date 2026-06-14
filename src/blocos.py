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


class BlocoRepetir(Bloco):
    """Counted loop block that groups sub-commands and repeats them n times."""

    def __init__(self, x, y, n=2):
        super().__init__(x, y, 80, 30, (220, 130, 0))
        self.tipo = "repetir"
        self.n = n
        self.comandos = []
        self.clicado = False

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)
        pygame.draw.rect(superficie, (160, 90, 0), self.rect, 2)
        fonte = pygame.font.SysFont(None, 18)
        texto = fonte.render(f"Rep x{self.n}", True, (255, 255, 255))
        superficie.blit(texto, (self.rect.x + 5, self.rect.y + 8))
















