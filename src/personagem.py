import pygame
from src.configuracao import TAMANHO_CELULA, CORES

class Personagem:
    def __init__(self, x_inicio, y_inicio):
        self.x = x_inicio
        self.y = y_inicio
        self.executando_comandos = False
        self.indice_comando_atual = 0
        self.passos_restantes = 0
        self.direcao_atual = None

    def desenhar(self, superficie):
        pygame.draw.circle(superficie, (0, 255, 0), (self.x, self.y), 15)

    def iniciar_programacao(self):
        self.executando_comandos = True
        self.indice_comando_atual = 0
        self.passos_restantes = 0

    def atualizar_movimento(self, lista_pecas):
        if not self.executando_comandos:
            return

        if self.passos_restantes <= 0:
            if self.indice_comando_atual < len(lista_pecas):
                peca_atual = lista_pecas[self.indice_comando_atual]
                self.direcao_atual = peca_atual.tipo
                self.passos_restantes = 10  # Ajustado para caminhar uma distância melhor no campo reduzido
                self.indice_comando_atual += 1
            else:
                self.executando_comandos = False
                self.direcao_atual = None

        if self.passos_restantes > 0:
            velocidade = 3
            if self.direcao_atual == "esquerda" and self.x > 20: # Limites do campo isolado
                self.x -= velocidade
            elif self.direcao_atual == "direita" and self.x < 620:
                self.x += velocidade
            elif self.direcao_atual == "cima" and self.y > 20:
                self.y -= velocidade
            elif self.direcao_atual == "baixo" and self.y < 180:
                self.y += velocidade
            self.passos_restantes -= 1
