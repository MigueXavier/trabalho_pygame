import pygame
from sys import exit
import copy

from src.configuracao import *
from src.personagem import Personagem
from src.blocos import BlocoEsquerda, BlocoDireita, BlocoCima, BlocoBaixo, BlocoRepetir
from src.comandos import BotaoDeploy, BotaoReset, Botao
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

        self.personagem = None
        for linha in self.matriz:
            for celula in linha:
                if isinstance(celula, Personagem):
                    self.personagem = celula
                    break

        if self.personagem is None:
            self.personagem = Personagem(0, 0)

        self.pontuacao = Pontuacao()
        self.fonte = pygame.font.Font(None, 36)

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
        

        # ── Bloco de repetição + controles de n ─────────────────────
        # Linha 3 (y=160): [−] n [+] | [Repetir]
        self.n_repeticoes = 2
        self.modo_loop = False
        self.loop_ativo = None

        self.bloco_repetir_paleta = BlocoRepetir(grade_x + bloco_w + gap, 160, n=self.n_repeticoes)
        self.botao_menos = Botao(grade_x,           163, 22, 26, (100, 100, 100))
        self.botao_mais  = Botao(grade_x + 25,      163, 22, 26, (100, 100, 100))
        # "Fechar Loop" button – only active during loop recording mode
        self.botao_fechar_loop = Botao(centro - 75, 213, 150, 30, (0, 160, 0))

        # Font cached for UI labels (created once after pygame.init)
        self._fonte_ui = pygame.font.SysFont(None, 20)

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

        # --- Fonte maior e em negrito para os avisos de fim de jogo ---
        self.fonte_status = pygame.font.SysFont("Arial", 50, bold=True)

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                pygame.quit()
                exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = evento.pos

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = evento.pos

                if self.modo_loop:
                    # ── Loop recording mode: direction blocks add to loop ──
                    if self.bloco_direita.checar_clique(pos_mouse):
                        self.loop_ativo.comandos.append(self.bloco_direita.clonar_bloco())
                    elif self.bloco_esquerda.checar_clique(pos_mouse):
                        self.loop_ativo.comandos.append(self.bloco_esquerda.clonar_bloco())
                    elif self.bloco_cima.checar_clique(pos_mouse):
                        self.loop_ativo.comandos.append(self.bloco_cima.clonar_bloco())
                    elif self.bloco_baixo.checar_clique(pos_mouse):
                        self.loop_ativo.comandos.append(self.bloco_baixo.clonar_bloco())
                    elif self.botao_fechar_loop.checar_clique(pos_mouse):
                        self._fechar_loop()
                    elif self.botao_reset.checar_clique(pos_mouse):
                        self._reset_completo()
                else:
                    # ── Normal mode ───────────────────────────────────────
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
                    elif self.bloco_repetir_paleta.checar_clique(pos_mouse):
                        self._iniciar_loop()
                    elif self.botao_deploy.checar_clique(pos_mouse):
                        self.botao_deploy.acao(self.personagem, self.lista_pecas, self.pontuacao)
                    elif self.botao_reset.checar_clique(pos_mouse):
                        self._reset_completo()
                    elif self.botao_menos.checar_clique(pos_mouse):
                        self.n_repeticoes = max(1, self.n_repeticoes - 1)
                        self.bloco_repetir_paleta.n = self.n_repeticoes
                    elif self.botao_mais.checar_clique(pos_mouse):
                        self.n_repeticoes = min(9, self.n_repeticoes + 1)
                        self.bloco_repetir_paleta.n = self.n_repeticoes

    def atualizar(self):
        self.personagem.atualizar_movimento(self.matriz)

    # ── Loop helpers ────────────────────────────────────────────────────────

    def _iniciar_loop(self):
        self.modo_loop = True
        self.loop_ativo = BlocoRepetir(0, 0, n=self.n_repeticoes)
        self.bloco_repetir_paleta.clicado = True
        self.bloco_repetir_paleta.cor = (110, 65, 0)

    def _fechar_loop(self):
        if self.loop_ativo is not None:
            self.lista_pecas.append(self.loop_ativo)
        self.modo_loop = False
        self.loop_ativo = None
        self.bloco_repetir_paleta.clicado = False
        self.bloco_repetir_paleta.cor = (220, 130, 0)

    def _reset_completo(self):
        self.botao_reset.acao(
            self.lista_pecas,
            self.bloco_direita, self.bloco_esquerda,
            self.bloco_cima, self.bloco_baixo,
        )
        self.modo_loop = False
        self.loop_ativo = None
        self.bloco_repetir_paleta.clicado = False
        self.bloco_repetir_paleta.cor = (220, 130, 0)
        self.pontuacao.resetar()

    # ── Drawing ─────────────────────────────────────────────────────────────

    def _desenhar_linha_translucida(self, y):
        """Desenha uma linha horizontal translúcida no painel direito."""
        surf = pygame.Surface((LARGURA_TELA - self.PAINEL_X, 2), pygame.SRCALPHA)
        surf.fill((255, 255, 255, 60))  # branco com ~24% opacidade
        self.tela.blit(surf, (self.PAINEL_X, y))

    def _desenhar_fila_comandos(self):
        """Draw the command queue; BlocoRepetir is rendered wide with sub-commands."""
        x = self.pos_x_inicial
        y = self.pos_y_lista
        
        for peca in self.lista_pecas:
            if peca is None:
                continue
            if getattr(peca, 'tipo', None) == 'repetir':
                n_sub = len(peca.comandos)
                largura = 80 + (n_sub * self.espacamento if n_sub > 0 else 0)
                peca.rect.x = x
                peca.rect.y = y
                peca.rect.width = largura
                peca.desenhar(self.tela)
                for i, cmd in enumerate(peca.comandos):
                    cmd.rect.x = x + 80 + i * self.espacamento
                    cmd.rect.y = y
                    cmd.desenhar(self.tela)
                x += largura + 10
            else:
                peca.rect.x = x
                peca.rect.y = y
                peca.desenhar(self.tela)
                x += self.espacamento

        # Show the in-progress loop block at the end of the queue
        if self.modo_loop and self.loop_ativo:
            n_sub = len(self.loop_ativo.comandos)
            largura = max(80, 80 + n_sub * self.espacamento)
            frame_rect = pygame.Rect(x, y, largura, 30)
            pygame.draw.rect(self.tela, (180, 100, 0), frame_rect)
            pygame.draw.rect(self.tela, (255, 200, 0), frame_rect, 2)
            label = self._fonte_ui.render(f"Rep x{self.loop_ativo.n}...", True, (255, 230, 150))
            self.tela.blit(label, (x + 4, y + 8))
            for i, cmd in enumerate(self.loop_ativo.comandos):
                cmd.rect.x = x + 80 + i * self.espacamento
                cmd.rect.y = y
                cmd.desenhar(self.tela)

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

        BORDA = 1
        total_cols = cols + 2 * BORDA
        total_rows = rows + 2 * BORDA

        offset_x = (self.PAINEL_X - total_cols * TAMANHO_CELULA) // 2
        offset_y = (ALTURA_TELA  - total_rows * TAMANHO_CELULA) // 2

        # 1. Desenha as paredes na borda externa
        for i in range(total_rows):
            for j in range(total_cols):
                x = offset_x + j * TAMANHO_CELULA
                y = offset_y + i * TAMANHO_CELULA
                sprite_p = self.objeto_matriz._sprite_parede(i, j, total_rows, total_cols)
                if sprite_p:
                    self.tela.blit(sprite_p, (x, y))

        # 2. Desenha o interior: Fundo + Linhas Divisórias + Entidades
        for i in range(rows):
            for j in range(cols):
              
                x = offset_x + (j + BORDA) * TAMANHO_CELULA
                y = offset_y + (i + BORDA) * TAMANHO_CELULA

               
                self.tela.blit(self.objeto_matriz.fundo, (x, y))

                # --- NOVA PARTE: Desenha a linha divisória ao redor da célula ---
                # Cor cinza escuro (40, 40, 40) 
                cor_da_linha = CORES["COR_LINHA"] 
                pygame.draw.rect(self.tela, cor_da_linha, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)
                

               
                celula = self.matriz[i][j]
                if celula is not None:
                    if isinstance(celula, Personagem):
                        
                        celula.desenhar(self.tela, x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)
                    else:
                        celula.desenhar(self.tela, x, y)
        # ── Painel direito ───────────────────────────────────────────
        self.bloco_cima.desenhar(self.tela)
        self.bloco_baixo.desenhar(self.tela)
        self.bloco_esquerda.desenhar(self.tela)
        self.bloco_direita.desenhar(self.tela)

        # Repeat block palette row: [−] n [+] | [Repetir]
        self.botao_menos.desenhar(self.tela)
        minus_lbl = self._fonte_ui.render("-", True, (255, 255, 255))
        self.tela.blit(minus_lbl, (self.botao_menos.rect.x + 7, self.botao_menos.rect.y + 5))

        self.botao_mais.desenhar(self.tela)
        plus_lbl = self._fonte_ui.render("+", True, (255, 255, 255))
        self.tela.blit(plus_lbl, (self.botao_mais.rect.x + 6, self.botao_mais.rect.y + 5))

        n_lbl = self._fonte_ui.render(str(self.n_repeticoes), True, (255, 255, 255))
        n_x = self.botao_menos.rect.right + 3
        self.tela.blit(n_lbl, (n_x, self.botao_menos.rect.y + 5))

        self.bloco_repetir_paleta.desenhar(self.tela)

        # "Fechar Loop" button – only shown during loop recording
        if self.modo_loop:
            self.botao_fechar_loop.desenhar(self.tela)
            fechar_lbl = self._fonte_ui.render("Fechar Loop", True, (255, 255, 255))
            self.tela.blit(fechar_lbl, (
                self.botao_fechar_loop.rect.x + 20,
                self.botao_fechar_loop.rect.y + 8,
            ))

        self.botao_deploy.desenhar(self.tela)
        self.botao_reset.desenhar(self.tela)

        # Fila de comandos
        self._desenhar_fila_comandos()

        texto = self.fonte.render(
            f"Pontos: {self.pontuacao.pontos}", True, (255, 255, 255))
        self.tela.blit(texto, (10, 10))



        if self.personagem.chegou_no_objetivo:
            surf_texto = self.fonte_status.render("PARABÉNS!", True, (0, 255, 0))
           
            rect_texto = surf_texto.get_rect(center=(self.PAINEL_X // 2, ALTURA_TELA // 6))
            self.tela.blit(surf_texto, rect_texto)

    
        elif self.personagem.vidas <= 0:
            surf_texto = self.fonte_status.render("GAME OVER", True, (255, 0, 0))
            rect_texto = surf_texto.get_rect(center=(self.PAINEL_X // 2, ALTURA_TELA // 6))
            self.tela.blit(surf_texto, rect_texto)


        pygame.display.update()

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)