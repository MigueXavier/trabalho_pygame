import pygame
from sys import exit
from src.configuracao import *


class Botao:
    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)

    def checar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
    
class BotaoDeploy(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 120, 35, (0, 0, 200))

    def acao(self, personagem_alvo, lista_pecas):
        personagem_alvo.iniciar_programacao(lista_pecas)
class BotaoReset(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 120, 35, (200, 200, 0))

    def acao(self, lista_pecas, botao_verde, botao_vermelho, botao_cima, botao_baixo):
        
        lista_pecas.clear()
        botao_verde.cor = (0, 200, 0)
        botao_vermelho.cor = (200, 0, 0)
        botao_cima.cor = (200, 0, 200)
        botao_baixo.cor = (0, 200, 200)
        botao_verde.clicado = False
        botao_vermelho.clicado = False
        botao_cima.clicado = False
        botao_baixo.clicado = False