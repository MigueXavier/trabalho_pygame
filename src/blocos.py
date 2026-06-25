import pygame
import copy
from sys import exit
from src.configuracao import *


class Bloco:

    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor
     
        pygame.font.init()
        self.fonte = pygame.font.Font(resource_path("assets/fontes/PressStart2P.ttf"), 14)

    def __deepcopy__(self, memo):
        cls = self.__class__
        novo = cls.__new__(cls)
        memo[id(self)] = novo
        for k, v in self.__dict__.items():
            if isinstance(v, pygame.font.Font):
                setattr(novo, k, pygame.font.Font(resource_path("assets/fontes/PressStart2P.ttf"), 14))
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
        super().__init__(x, y, 80, 30, CORES["AZUL_MARINHO"])
        self.tipo = "direita"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = CORES["AZUL_MARINHO_ESCURO"]


class BlocoEsquerda(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, CORES["AZUL_MARINHO"])
        self.tipo = "esquerda"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = CORES["AZUL_MARINHO_ESCURO"]


class BlocoCima(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, CORES["AZUL_MARINHO"])
        self.tipo = "cima"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = CORES["AZUL_MARINHO_ESCURO"]


class BlocoBaixo(Bloco):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, CORES["AZUL_MARINHO"])
        self.tipo = "baixo"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = CORES["AZUL_MARINHO_ESCURO"]


class BlocoRepetir(Bloco):

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