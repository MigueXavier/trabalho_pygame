import pygame
import copy
from sys import exit
from src.configuracao import *


class Bloco:
    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
     
        pygame.font.init()
        self.fonte = pygame.font.Font("assets/fontes/PressStart2P.ttf", 14)

    def __deepcopy__(self, memo):
        cls = self.__class__
        novo = cls.__new__(cls)
        memo[id(self)] = novo
        for k, v in self.__dict__.items():
            if isinstance(v, pygame.font.Font):
                setattr(novo, k, pygame.font.Font("assets/fontes/PressStart2P.ttf", 14))
            else:
                setattr(novo, k, copy.deepcopy(v, memo))
        return novo

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)
        pygame.draw.rect(superficie, (255, 255, 255), self.rect, 1)

        if hasattr(self, 'tipo'):
            setas = {
                "direita": "→",
                "esquerda": "←",
                "cima": "↑",
                "baixo": "↓"
            }
            
            if self.tipo in setas:
                texto_sinal = setas[self.tipo]
                superficie_texto = self.fonte.render(texto_sinal, True, (255, 255, 255))
                rect_texto = superficie_texto.get_rect(center=self.rect.center)
                superficie.blit(superficie_texto, rect_texto)

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
















