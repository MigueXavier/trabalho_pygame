import pygame
from sys import exit
import copy
import json

from src.configuracao import *
from src.personagem import Personagem
from src.blocos import BlocoEsquerda, BlocoDireita, BlocoCima, BlocoBaixo, BlocoRepetir
from src.comandos import BotaoDeploy, BotaoReset, Botao
from src.matriz import Matriz
from src.pontuacao import Pontuacao
from src.menu import carregar_fonte

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Perdido no Algoritmo - Protótipo")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.faseAtual = 1
        with open(f"fases/fase_{self.faseAtual}.json", "r", encoding="utf-8") as arquivo:
            dados_fase = json.load(arquivo)
        self.dados = dados_fase
        self.objeto_matriz = Matriz(dados_fase)
        self.matriz = self.objeto_matriz.matriz
        self.acao_final = None
        self.inicializar_elementos()

    def inicializar_elementos(self):

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


        self.PAINEL_X = LARGURA_TELA // 2


        centro = self.PAINEL_X + (LARGURA_TELA - self.PAINEL_X) // 2


        bloco_w, bloco_h = 80, 30
        gap = 10
        grade_x = centro - bloco_w - gap // 2
        y_inicial = 80

        classes_blocos = {
            "cima": BlocoCima,
            "baixo": BlocoBaixo,
            "esquerda": BlocoEsquerda,
            "direita": BlocoDireita
        }

        self.blocos_paleta = {}
        

        blocos_fase = self.dados.get("blocos_disponiveis", ["cima", "baixo", "esquerda", "direita"])


        idx_direcional = 0
        for indice, nome_bloco in enumerate(blocos_fase):
            if nome_bloco == "repetir":
                continue
                
            if nome_bloco in classes_blocos:
                linha = idx_direcional // 2
                coluna = idx_direcional % 2

                x_dinamico = grade_x + coluna * (bloco_w + gap)
                y_dinamico = y_inicial + linha * (bloco_h + gap)




                ClasseDoBloco = classes_blocos[nome_bloco]
                bloco_instanciado = ClasseDoBloco(x_dinamico, y_dinamico)



                chave_unica = f"{nome_bloco}_{indice}"
                self.blocos_paleta[chave_unica] = bloco_instanciado
                
                idx_direcional += 1


        self.n_repeticoes = 2
        self.modo_loop = False
        self.loop_ativo = None


        linhas_totais = (len(self.blocos_paleta) + 1) // 2
        y_repetir = y_inicial + linhas_totais * (bloco_h + gap)

        self.bloco_repetir_paleta = BlocoRepetir(grade_x + bloco_w + gap, y_repetir, n=self.n_repeticoes)
        self.botao_menos = Botao(grade_x,           y_repetir + 3, 22, 26, (100, 100, 100))
        self.botao_mais  = Botao(grade_x + 25,      y_repetir + 3, 22, 26, (100, 100, 100))
        self.botao_fechar_loop = Botao(centro - 75, y_repetir + 53, 150, 30, (0, 160, 0))


        self._fonte_ui = pygame.font.SysFont(None, 20)


        self.lista_pecas    = []
        self.pos_x_inicial  = self.PAINEL_X + 10
        self.pos_y_lista    = 290
        self.espacamento    = 90


        btn_w = 120
        btn_gap = 20
        btn_total = btn_w * 2 + btn_gap
        btn_x = centro - btn_total // 2
        self.botao_deploy = BotaoDeploy(btn_x,           530)
        self.botao_reset  = BotaoReset( btn_x + btn_w + btn_gap, 530)


        self.sep_y = [200, 270, 510]

        self.fonte_status = carregar_fonte(27)
        self.fonte_resultado = carregar_fonte(12)
        self.fonte_botao_resultado = carregar_fonte(13)
        self.estado_resultado = None

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.acao_final = "sair"
                self.rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.estado_resultado:
                self._processar_clique_resultado(evento.pos)
                continue

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = evento.pos

                if self.modo_loop:

                    clicou_bloco = False
                    for nome, bloco in self.blocos_paleta.items():
                        if bloco.checar_clique(pos_mouse):
                            self.loop_ativo.comandos.append(bloco.clonar_bloco())
                            clicou_bloco = True
                            break
                    
                    if not clicou_bloco:
                        if self.botao_fechar_loop.checar_clique(pos_mouse):
                            self._fechar_loop()
                        elif self.botao_reset.checar_clique(pos_mouse):
                            self._reset_completo()
                else:

                    clicou_bloco = False
                    for nome, bloco in self.blocos_paleta.items():
                        if bloco.checar_clique(pos_mouse) and not bloco.clicado:
                            self.lista_pecas.append(bloco.clonar_bloco())
                            bloco.acao()
                            clicou_bloco = True
                            break
                    
                    if not clicou_bloco:

                        blocos_fase = self.dados.get("blocos_disponiveis", [])
                        if "repetir" in blocos_fase and self.bloco_repetir_paleta.checar_clique(pos_mouse):
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
        if self.estado_resultado:
            return
        self.personagem.atualizar_movimento(self.matriz)
        if self.personagem.chegou_no_objetivo:
            self.estado_resultado = "vitoria"
        elif self.personagem.vidas <= 0:
            self.estado_resultado = "derrota"

    def _obter_botoes_resultado(self):
        largura, altura = 240, 44
        x = (LARGURA_TELA - largura) // 2
        if self.estado_resultado == "vitoria":
            opcoes = [
                ("Próxima Fase", "proxima_fase"),
                ("Repetir Fase", "repetir_fase"),
                ("Menu Principal", "menu_principal"),
            ]
        else:
            opcoes = [
                ("Tentar Novamente", "repetir_fase"),
                ("Menu Principal", "menu_principal"),
            ]
        inicio_y = 285 if len(opcoes) == 3 else 310
        return [
            (pygame.Rect(x, inicio_y + indice * 58, largura, altura), texto, acao)
            for indice, (texto, acao) in enumerate(opcoes)
        ]

    def _reiniciar_fase(self):
        self.objeto_matriz = Matriz(self.dados)
        self.matriz = self.objeto_matriz.matriz
        self.inicializar_elementos()
        self.personagem.linha = self.personagem.linha_inicial
        self.personagem.coluna = self.personagem.coluna_inicial
        self.personagem.vidas = 3
        self.personagem.chegou_no_objetivo = False
        self.personagem.executando_comandos = False
        self.personagem.indice_comando_atual = 0
        self.personagem.comandos_expandidos = []

    def _processar_clique_resultado(self, pos_mouse):
        for rect, _, acao in self._obter_botoes_resultado():
            if not rect.collidepoint(pos_mouse):
                continue
            if acao == "repetir_fase":
                self._reiniciar_fase()
            else:
                self.acao_final = acao
                self.rodando = False
            return

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

        self.botao_reset.acao(self.lista_pecas, self.blocos_paleta)
        

        self.modo_loop = False
        self.loop_ativo = None
        self.bloco_repetir_paleta.clicado = False
        self.bloco_repetir_paleta.cor = (220, 130, 0)
        self.pontuacao.resetar()

    def _desenhar_linha_translucida(self, y):
        surf = pygame.Surface((LARGURA_TELA - self.PAINEL_X, 2), pygame.SRCALPHA)
        surf.fill((255, 255, 255, 60))
        self.tela.blit(surf, (self.PAINEL_X, y))

    def _desenhar_fila_comandos(self):
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


        pygame.draw.line(self.tela, CORES["COR_LINHA"],
                         (self.PAINEL_X, 0), (self.PAINEL_X, ALTURA_TELA), 2)


        for y in self.sep_y:
            self._desenhar_linha_translucida(y)


        cols = len(self.matriz[0])
        rows = len(self.matriz)

        BORDA = 1
        total_cols = cols + 2 * BORDA
        total_rows = rows + 2 * BORDA

        offset_x = (self.PAINEL_X - total_cols * TAMANHO_CELULA) // 2
        offset_y = (ALTURA_TELA  - total_rows * TAMANHO_CELULA) // 2


        for i in range(total_rows):
            for j in range(total_cols):
                x = offset_x + j * TAMANHO_CELULA
                y = offset_y + i * TAMANHO_CELULA
                sprite_p = self.objeto_matriz._sprite_parede(i, j, total_rows, total_cols)
                if sprite_p:
                    self.tela.blit(sprite_p, (x, y))


        for i in range(rows):
            for j in range(cols):
                x = offset_x + (j + BORDA) * TAMANHO_CELULA
                y = offset_y + (i + BORDA) * TAMANHO_CELULA

                self.tela.blit(self.objeto_matriz.fundo, (x, y))

                cor_da_linha = CORES["COR_LINHA"] 
                pygame.draw.rect(self.tela, cor_da_linha, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 2)

                celula = self.matriz[i][j]
                if celula is not None:
                    if isinstance(celula, Personagem):
                        celula.desenhar(self.tela, x + TAMANHO_CELULA // 2, y + TAMANHO_CELULA // 2)
                    else:
                        celula.desenhar(self.tela, x, y)


        for bloco in self.blocos_paleta.values():
            bloco.desenhar(self.tela)


        blocos_fase = self.dados.get("blocos_disponiveis", [])
        if "repetir" in blocos_fase:
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

            if self.modo_loop:
                self.botao_fechar_loop.desenhar(self.tela)
                fechar_lbl = self._fonte_ui.render("Fechar Loop", True, (255, 255, 255))
                self.tela.blit(fechar_lbl, (
                    self.botao_fechar_loop.rect.x + 20,
                    self.botao_fechar_loop.rect.y + 8,
                ))

        self.botao_deploy.desenhar(self.tela)
        self.botao_reset.desenhar(self.tela)

        self._desenhar_fila_comandos()

        texto = self.fonte.render(f"Pontos: {self.pontuacao.pontos}", True, (255, 255, 255))
        self.tela.blit(texto, (10, 10))

        if self.estado_resultado:
            self._desenhar_tela_resultado()

        pygame.display.update()

    def _desenhar_tela_resultado(self):
        sobreposicao = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 185))
        self.tela.blit(sobreposicao, (0, 0))

        painel = pygame.Rect(390, 130, 420, 350)
        pygame.draw.rect(self.tela, (25, 30, 55), painel)
        pygame.draw.rect(self.tela, (170, 190, 255), painel, 3)

        if self.estado_resultado == "vitoria":
            titulo, cor, descricoes = "RODOU LISO!", (80, 230, 130), (
                "Código sem bugs!",
            )
        else:
            titulo, cor, descricoes = "GAME OVER!", (240, 90, 90), (
                "Você está a um laço",
                "da vitória!",
            )

        titulo_surface = self.fonte_status.render(titulo, True, cor)
        titulo_rect = titulo_surface.get_rect(center=(LARGURA_TELA // 2, 195))
        self.tela.blit(titulo_surface, titulo_rect)

        for indice, descricao in enumerate(descricoes):
            descricao_surface = self.fonte_resultado.render(descricao, True, (255, 255, 255))
            descricao_rect = descricao_surface.get_rect(center=(LARGURA_TELA // 2, 235 + indice * 20))
            self.tela.blit(descricao_surface, descricao_rect)

        for rect, texto, _ in self._obter_botoes_resultado():
            hover = rect.collidepoint(pygame.mouse.get_pos())
            cor_botao = (75, 105, 180) if hover else (45, 65, 125)
            pygame.draw.rect(self.tela, cor_botao, rect)
            pygame.draw.rect(self.tela, (220, 230, 255), rect, 2)
            texto_surface = self.fonte_botao_resultado.render(texto, True, (255, 255, 255))
            texto_rect = texto_surface.get_rect(center=rect.center)
            self.tela.blit(texto_surface, texto_rect)

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)
        return self.acao_final
