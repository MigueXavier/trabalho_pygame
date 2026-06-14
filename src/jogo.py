import pygame
from sys import exit
import copy

from src.configuracao import *
from src.personagem import Personagem
from src.blocos import BlocoEsquerda, BlocoDireita, BlocoCima, BlocoBaixo
from src.comandos import BotaoDeploy, BotaoReset
from src.matriz import Matriz
from src.pontuacao import Pontuacao

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Perdido no Algoritmo - Protótipo")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.inicializar_elementos()

    def inicializar_elementos(self):
        self.objeto_matriz = Matriz()
        self.matriz = self.objeto_matriz.matriz
        self.pontuacao = Pontuacao()
        self.fonte = pygame.font.Font(None, 36)

        self.personagem = None
        for linha in self.matriz:
            for celula in linha:
                if isinstance(celula, Personagem):
                    self.personagem = celula
                    break

        if self.personagem is None:
            self.personagem = Personagem(0, 0)

        # Divisão da tela
        self.PAINEL_X = LARGURA_TELA // 2  # x=400

        # Centro do painel direito
        centro = self.PAINEL_X + (LARGURA_TELA - self.PAINEL_X) // 2  # x=600

        # ── Seção 1: Blocos de direção (grade 2x2) ──────────────────
        # Cada bloco: 80x30. Espaçamento horizontal: 10px entre colunas
        # Linha 1: Cima + Baixo   (y=80)
        # Linha 2: Esquerda + Direita (y=120)
        bloco_w, bloco_h = 80, 30
        gap = 10
        grade_x = centro - bloco_w - gap // 2  # x da coluna esquerda
        self.bloco_cima     = BlocoCima(    grade_x,              80)
        self.bloco_baixo    = BlocoBaixo(   grade_x + bloco_w + gap, 80)
        self.bloco_esquerda = BlocoEsquerda(grade_x,              80 + bloco_h + gap)
        self.bloco_direita  = BlocoDireita( grade_x + bloco_w + gap, 80 + bloco_h + gap)

        # ── Seção 2: Fila de comandos ────────────────────────────────
        self.lista_pecas    = []
        self.pos_x_inicial  = self.PAINEL_X + 10
        self.pos_y_lista    = 290   # abaixo da linha separadora do meio
        self.espacamento    = 90    # 80px bloco + 10px gap

        # ── Seção 3: Deploy + Reset ──────────────────────────────────
        # Dois botões de 120x35, separados por 20px, centralizados
        btn_w = 120
        btn_gap = 20
        btn_total = btn_w * 2 + btn_gap
        btn_x = centro - btn_total // 2
        self.botao_deploy = BotaoDeploy(btn_x,           530)
        self.botao_reset  = BotaoReset( btn_x + btn_w + btn_gap, 530)

        # Linhas separadoras do painel (y fixos)
        self.sep_y = [200, 270, 510]  # entre blocos/fila e fila/botões

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
        self.personagem.atualizar_movimento(
        self.lista_pecas,
        self.matriz,
        self.pontuacao
    )

    def _desenhar_linha_translucida(self, y):
        """Desenha uma linha horizontal translúcida no painel direito."""
        surf = pygame.Surface((LARGURA_TELA - self.PAINEL_X, 2), pygame.SRCALPHA)
        surf.fill((255, 255, 255, 60))  # branco com ~24% opacidade
        self.tela.blit(surf, (self.PAINEL_X, y))

    def desenhar(self):
        self.tela.fill(CORES["FUNDO"])

        # Linha divisória vertical principal
        pygame.draw.line(self.tela, CORES["COR_LINHA"],
                         (self.PAINEL_X, 0), (self.PAINEL_X, ALTURA_TELA), 2)

        # Linhas separadoras translúcidas no painel
        for y in self.sep_y:
            self._desenhar_linha_translucida(y)

        # ── Matriz à esquerda, centralizada ─────────────────────────
        cols = len(self.matriz[0])
        rows = len(self.matriz)
        offset_x = (self.PAINEL_X - cols * 50) // 2
        offset_y = (ALTURA_TELA  - rows * 50) // 2

        for i in range(rows):
            for j in range(cols):
                x = offset_x + j * 50
                y = offset_y + i * 50
                if self.matriz[i][j] is not None:
                    if isinstance(self.matriz[i][j], Personagem):
                        self.matriz[i][j].desenhar(self.tela, x + 25, y + 25)
                    else:
                        self.matriz[i][j].desenhar(self.tela, x, y)

        # ── Painel direito ───────────────────────────────────────────
        self.bloco_cima.desenhar(self.tela)
        self.bloco_baixo.desenhar(self.tela)
        self.bloco_esquerda.desenhar(self.tela)
        self.bloco_direita.desenhar(self.tela)

        self.botao_deploy.desenhar(self.tela)
        self.botao_reset.desenhar(self.tela)

        # Fila de comandos
        for indice, objeto_botao in enumerate(self.lista_pecas):
            objeto_botao.rect.x = self.pos_x_inicial + (indice * self.espacamento)
            objeto_botao.rect.y = self.pos_y_lista
            objeto_botao.desenhar(self.tela)

        texto = self.fonte.render(
            f"Pontos: {self.pontuacao.pontos}",True,(255, 255, 255))

        self.tela.blit(texto, (10, 10))

        pygame.display.update()

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)