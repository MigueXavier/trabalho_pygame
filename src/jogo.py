import pygame
from sys import exit
import copy

from src.configuracao import *
# Se já tiver separado os arquivos, descomente as linhas abaixo:
from src.personagem import Personagem
from src.blocos import BlocoEsquerda, BlocoDireita, BlocoCima, BlocoBaixo
from src.comandos import BotaoDeploy, BotaoReset

# [Mantenha aqui as definições das classes Personagem, Botao, BotaoVerde, etc., que estavam no seu test2.py]

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Perdido no Algoritmo - Protótipo")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.inicializar_elementos()

    def inicializar_elementos(self):
    
        self.personagem = Personagem(320, 100)
        self.bloco_esquerda = BlocoEsquerda(210, 210)
        self.bloco_direita = BlocoDireita(350, 210)
        self.bloco_cima = BlocoCima(210, 250)
        self.bloco_baixo = BlocoBaixo(350, 250)
        
        self.lista_pecas = []
        self.pos_x_inicial = 40
        self.pos_y_lista = 320
        self.espacamento = 95 

        self.botao_deploy = BotaoDeploy(190, 410)
        self.botao_reset = BotaoReset(320, 410)

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                pygame.quit()
                exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = evento.pos
                
                if self.bloco_direita.checar_clique(pos_mouse) and not self.bloco_direita.clicado:
                    self.lista_pecas.append(self.bloco_direita.clonar_bloco())
                    self.bloco_direita.acao()
                elif self.bloco_esquerda.checar_clique(pos_mouse) and not self.bloco_esquerda.clicado:
                    self.lista_pecas.append(self.bloco_esquerda.clonar_bloco())
                    self.bloco_esquerda.acao()
                elif self.bloco_cima.checar_clique(pos_mouse) and not self.bloco_cima.clicado:
                    self.lista_pecas.append(self.bloco_cima.clonar_bloco())
                    self.bloco_cima.acao()
                elif self.bloco_baixo.checar_clique(pos_mouse) and not self.bloco_baixo.clicado:
                    self.lista_pecas.append(self.bloco_baixo.clonar_bloco())
                    self.bloco_baixo.acao()
                elif self.botao_deploy.checar_clique(pos_mouse):
                     self.botao_deploy.acao(self.personagem)
                elif self.botao_reset.checar_clique(pos_mouse):
                     self.botao_reset.acao(self.lista_pecas, self.bloco_direita, self.bloco_esquerda, self.bloco_cima, self.bloco_baixo)

    def atualizar(self):
        self.personagem.atualizar_movimento(self.lista_pecas)

    def desenhar(self):
        self.tela.fill(CORES["FUNDO"])
        
   
        pygame.draw.line(self.tela, CORES["COR_LINHA"], (0, 200), (LARGURA_TELA, 200), 2)
        pygame.draw.line(self.tela, CORES["COR_LINHA"], (0, 290), (LARGURA_TELA, 290), 2)
        pygame.draw.line(self.tela, CORES["COR_LINHA"], (0, 385), (LARGURA_TELA, 385), 2)

        self.personagem.desenhar(self.tela)
        self.bloco_esquerda.desenhar(self.tela)
        self.bloco_direita.desenhar(self.tela)
        self.bloco_cima.desenhar(self.tela)
        self.bloco_baixo.desenhar(self.tela)
        self.botao_deploy.desenhar(self.tela)
        self.botao_reset.desenhar(self.tela)

        # Desenhar a fila de comandos dinamicamente
        for indice, objeto_botao in enumerate(self.lista_pecas):
            objeto_botao.rect.x = self.pos_x_inicial + (indice * self.espacamento)
            objeto_botao.rect.y = self.pos_y_lista
            objeto_botao.desenhar(self.tela)

        pygame.display.update()

    def rodar(self):
        """Loop principal do jogo chamando os métodos modulares"""
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)