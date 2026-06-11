import copy
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((640, 480), 0, 32)
clock = pygame.time.Clock() 

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


class Botao:
    def __init__(self, x, y, largura, altura, cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = cor

    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)

    def checar_clique(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)
    
    def clonar_botao(self):
         return copy.deepcopy(self)


class BotaoVerde(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (0, 200, 0))
        self.tipo = "direita"
        self.clicado = False

    def acao(self):
        if not self.clicado:
         self.clicado = True
         self.cor = (0, 100, 0)


class BotaoVermelho(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (200, 0, 0))
        self.tipo = "esquerda"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = (100, 0, 0)
class BotaoCima(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (200, 0, 200))
        self.tipo = "cima"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = (100, 0, 100)
class BotaoBaixo(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 30, (0, 200, 200))
        self.tipo = "baixo"
        self.clicado = False

    def acao(self):
        if not self.clicado:
            self.clicado = True
            self.cor = (0, 100, 100)

class BotaoDeploy(Botao):
    def __init__(self, x, y):
        super().__init__(x, y, 120, 35, (0, 0, 200))

    def acao(self, personagem_alvo):
        personagem_alvo.iniciar_programacao()
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



personagem = Personagem(320, 100)


botao_vermelho = BotaoVermelho(210, 210)
botao_verde = BotaoVerde(350, 210)
botao_cima = BotaoCima(210, 250)
botao_baixo = BotaoBaixo(350, 250)

lista_pecas = []
pos_x_inicial = 40
pos_y_lista = 320
espacamento = 95 

botao_deploy = BotaoDeploy(190, 410)
botao_reset = BotaoReset(320, 410)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if botao_verde.checar_clique(event.pos):
                    if not botao_verde.clicado:
                     nova_peca = botao_verde.clonar_botao()
                     botao_verde.acao()
                     lista_pecas.append(nova_peca)
                elif botao_vermelho.checar_clique(event.pos):
                    if not botao_vermelho.clicado:
                     nova_peca = botao_vermelho.clonar_botao()
                     botao_vermelho.acao()
                     lista_pecas.append(nova_peca)
                elif botao_cima.checar_clique(event.pos):
                    if not botao_cima.clicado:
                        nova_peca = botao_cima.clonar_botao()
                        botao_cima.acao()
                        lista_pecas.append(nova_peca)
                elif botao_baixo.checar_clique(event.pos):
                    if not botao_baixo.clicado:
                        nova_peca = botao_baixo.clonar_botao()
                        botao_baixo.acao()
                        lista_pecas.append(nova_peca)
                elif botao_deploy.checar_clique(event.pos):
                     botao_deploy.acao(personagem)
                elif botao_reset.checar_clique(event.pos):
                     botao_reset.acao(lista_pecas, botao_verde, botao_vermelho, botao_cima, botao_baixo)

    personagem.atualizar_movimento(lista_pecas)

    screen.fill((20, 20, 20))
    
   
    pygame.draw.line(screen, (50, 50, 50), (0, 200), (640, 200), 2)  # Fim do campo de jogo
    pygame.draw.line(screen, (50, 50, 50), (0, 290), (640, 290), 2)  # Fim da seleção de movimentos
    pygame.draw.line(screen, (50, 50, 50), (0, 385), (640, 385), 2)  # Fim da lista/Início do Deploy

   
    personagem.desenhar(screen)
    botao_verde.desenhar(screen)
    botao_vermelho.desenhar(screen)
    botao_cima.desenhar(screen)
    botao_baixo.desenhar(screen)
    botao_deploy.desenhar(screen)
    botao_reset.desenhar(screen)

   
    for indice, objeto_botao in enumerate(lista_pecas):
        objeto_botao.rect.x = pos_x_inicial + (indice * espacamento)
        objeto_botao.rect.y = pos_y_lista
        objeto_botao.desenhar(screen)

    pygame.display.update()
    clock.tick(60)