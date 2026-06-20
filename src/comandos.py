import pygame
import json
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

    def acao(self, personagem_alvo, lista_pecas, pontuacao=None):
        personagem_alvo.iniciar_programacao(lista_pecas, pontuacao)
class BotaoReset(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 120, 35, (200, 200, 0))

    def acao(self, lista_pecas, blocos_paleta):
        
        lista_pecas.clear()
        
        # 2. Percorre dinamicamente todos os blocos que existem na fase atual
        for bloco in blocos_paleta.values():
            if bloco is not None and bloco.clicado:
                bloco.clicado = False
                
                # Reseta para a cor original do bloco. 
                # (Se cada classe de bloco tiver sua própria cor padrão definida no __init__ dela,
                # você pode até criar um método bloco.resetar() se preferir, ou definir uma cor fixa aqui)
                bloco.cor = CORES["AZUL_MARINHO"]