import pygame
from sys import exit
import copy
import json
import math

from src.configuracao import *
from src.personagem import Personagem
from src.blocos import BlocoEsquerda, BlocoDireita, BlocoCima, BlocoBaixo, BlocoRepetir
from src.comandos import BotaoDeploy, BotaoReset, Botao
from src.menu import carregar_fonte, BotaoMenu
from src.matriz import Matriz
from src.pontuacao import Pontuacao
from src.menu import carregar_fonte

class Jogo:
    def __init__(self, fase=1):
        if not pygame.get_init():
            pygame.init()   
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("assets/sons/musica_fundo.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

        self.som_clique = pygame.mixer.Sound("assets/sons/clique_botoes.mp3")
        self.som_clique.set_volume(0.4)

        self.som_passou_fase = pygame.mixer.Sound("assets/sons/next_level.mp3")
        self.som_passou_fase.set_volume(0.30)

        self.som_game_over = pygame.mixer.Sound("assets/sons/game_over.mp3")
        self.som_game_over.set_volume(0.30)

        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Perdido no Algoritmo - Protótipo")
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self.faseAtual = fase
        with open(f"fases/fase_{self.faseAtual}.json", "r", encoding="utf-8") as arquivo: 
            dados_fase = json.load(arquivo)
        self.dados = dados_fase
        self.objeto_matriz = Matriz(dados_fase)
        self.matriz = self.objeto_matriz.matriz
        self.acao_final = None
        self.inicializar_elementos()

    def inicializar_elementos(self):
    
        # Localiza o personagem dentro da matriz gerada
        self.personagem = None
        for linha in self.matriz:
            for celula in linha:
                if isinstance(celula, Personagem):
                    self.personagem = celula
                    break

        if self.personagem is None:
            self.personagem = Personagem(0, 0)

        self.pontuacao = Pontuacao()
        self.personagem._pontuacao = self.pontuacao
        self.fonte = pygame.font.Font(None, 36)

        # Divisão da tela
        self.PAINEL_X = LARGURA_TELA // 2  # x=400

        # Centro do painel direito
        centro = self.PAINEL_X + (LARGURA_TELA - self.PAINEL_X) // 2  # x=600
        painel_largura = LARGURA_TELA - self.PAINEL_X
        self.PAINEL_LARGURA = painel_largura

        topo = int(ALTURA_TELA * 0.03)

        self.area_como_jogar = pygame.Rect(
            self.PAINEL_X + margem,
            topo,
            self.PAINEL_LARGURA - margem * 2,
            int(ALTURA_TELA * PROP_COMO_JOGAR)
        )

        self.area_blocos = pygame.Rect(
            self.PAINEL_X + margem,
            self.area_como_jogar.bottom + topo,
            self.PAINEL_LARGURA - margem * 2,
            int(ALTURA_TELA * PROP_BLOCOS)
        )

        
        self.LARGURA_ACOES = 160
        gap_entre_caixas = 12

        self.area_sequencia = pygame.Rect(
            self.PAINEL_X + margem,
            self.area_blocos.bottom + topo,
            self.PAINEL_LARGURA - margem * 2 - self.LARGURA_ACOES - gap_entre_caixas,
            int(ALTURA_TELA * PROP_SEQUENCIA)
        )

        self.area_acoes = pygame.Rect(
            self.area_sequencia.right + gap_entre_caixas,
            self.area_sequencia.y,
            self.LARGURA_ACOES,
            self.area_sequencia.height
        )

        
        bloco_w = 80
        bloco_h = 35

        y_inicial = self.area_blocos.centery - bloco_h // 2 - 10

        classes_blocos = {
            "cima": BlocoCima,
            "baixo": BlocoBaixo,
            "esquerda": BlocoEsquerda,
            "direita": BlocoDireita
        }

        self.blocos_paleta = {}

        # Recupera a lista do JSON através do objeto matriz
        blocos_fase = self.dados.get("blocos_disponiveis", ["cima", "baixo", "esquerda", "direita"])

        tem_repetir = "repetir" in blocos_fase

        # Conta quantos itens direcionais existem (ignorando "repetir", que é tratado à parte)
        nomes_direcionais = [nome for nome in blocos_fase if nome in classes_blocos]
        total_itens = len(nomes_direcionais) + (1 if tem_repetir else 0)

        # Divide a largura da caixa de blocos em "total_itens" espaços iguais
        # Divide a largura ÚTIL da caixa (com margem nas duas pontas) em "total_itens" espaços iguais
        margem_lateral = 20
        largura_disponivel = self.area_blocos.width - margem_lateral * 2
        largura_slot = largura_disponivel // max(total_itens, 1)

        # Centraliza cada bloco dentro do seu próprio "slot", já considerando a margem lateral
        x_inicial = self.area_blocos.x + margem_lateral + (largura_slot - bloco_w) // 2

        idx_item = 0

        for indice, nome_bloco in enumerate(blocos_fase):

            if nome_bloco not in classes_blocos:
                continue

            x_dinamico = x_inicial + idx_item * largura_slot
            y_dinamico = y_inicial

            ClasseDoBloco = classes_blocos[nome_bloco]
            bloco_instanciado = ClasseDoBloco(
                x_dinamico,
                y_dinamico
            )

            chave_unica = f"{nome_bloco}_{indice}"

            self.blocos_paleta[chave_unica] = bloco_instanciado

            idx_item += 1

        
        self.n_repeticoes = 2
        self.modo_loop = False
        self.loop_ativo = None

        y_repetir = y_inicial
        pos_loop_x = x_inicial + idx_item * largura_slot

        self.bloco_repetir_paleta = BlocoRepetir(pos_loop_x, y_repetir, n=self.n_repeticoes)

        # Largura total ocupada pelos dois botões + espaço do número no meio
        largura_controles = 22 + 25 + 22   # botão-menos + espaço-do-número + botão-mais
        centro_bloco_repetir = pos_loop_x + bloco_w // 2
        x_controles = centro_bloco_repetir - largura_controles // 2

        self.botao_menos = Botao(x_controles,             y_repetir + bloco_h + 5, 22, 26, (100, 100, 100))
        self.botao_mais  = Botao(x_controles + 22 + 25,    y_repetir + bloco_h + 5, 22, 26, (100, 100, 100))

        fechar_loop_altura = 26
        fechar_loop_y = self.area_blocos.bottom - fechar_loop_altura - 8
        self.botao_fechar_loop = Botao(centro - 75, fechar_loop_y, 150, fechar_loop_altura, (0, 160, 0))

        # Font cached for UI labels
        
        self._fonte_ui = pygame.font.SysFont(None, 20)
        self._fonte_titulo_painel = pygame.font.SysFont(None, 24, bold=True)
        self._fonte_setas_texto = pygame.font.Font("assets/fontes/PressStart2P.ttf", 10)
        self._fonte_como_jogar = pygame.font.SysFont(None, 17)

        # ── Seção 2: Fila de comandos ────────────────────────────────
        self.lista_pecas    = []
        self.pos_x_inicial  = self.PAINEL_X + 10
        self.pos_y_lista    = 350   # abaixo da linha separadora do meio
        self.espacamento    = 90    # 80px bloco + 10px gap

        
        btn_w = self.area_acoes.width - 30
        btn_h = 44
        btn_gap_vertical = 14       
        btn_gap_divisor = 36        
        btn_x = self.area_acoes.x + 15

        
        altura_total_botoes = (btn_h * 3) + btn_gap_vertical + btn_gap_divisor
        primeiro_botao_y = self.area_acoes.centery - altura_total_botoes // 2

        self.botao_deploy = BotaoMenu(btn_x, primeiro_botao_y, btn_w, btn_h, "")
        self.botao_reset = BotaoMenu(btn_x, primeiro_botao_y + (btn_h + btn_gap_vertical), btn_w, btn_h, "")

      
        self.y_divisor_acoes = self.botao_reset.rect.bottom + 18

        
        espaco_restante_y = self.area_acoes.bottom - self.y_divisor_acoes
        y_sair = self.y_divisor_acoes + (espaco_restante_y - btn_h) // 2

        self.botao_sair = BotaoMenu(btn_x, y_sair, btn_w, btn_h, "")
    

        self._fonte_botoes_acoes = pygame.font.Font("assets/fontes/PressStart2P.ttf", 12)
    
        self._fonte_botoes_acoes = pygame.font.Font("assets/fontes/PressStart2P.ttf", 12)

        # Ícones dos botões de ação (carregados como imagem, em vez de desenhados manualmente)
        tamanho_icone = 16
        self._icone_play = pygame.transform.scale(
            pygame.image.load("assets/sprites/icones/play.png").convert_alpha(),
            (tamanho_icone, tamanho_icone)
        )
        self._icone_reset = pygame.transform.scale(
            pygame.image.load("assets/sprites/icones/reset.png").convert_alpha(),
            (tamanho_icone, tamanho_icone)
        )

        self.fonte_status = carregar_fonte(27)
        self.fonte_resultado = carregar_fonte(12)
        self.fonte_botao_resultado = carregar_fonte(13)
        self.estado_resultado = None

        self.instrucoes = []

        self._drag_item = None
        self._drag_offset = (0, 0)
        self._drag_pos = (0, 0)
        self._drag_indice_origem = None
        self._drag_iniciou_em = (0, 0)
        self._drag_ativo = False

        self.scroll_y = 0
        self.altura_conteudo = 0

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.acao_final = "sair"
                self.rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.estado_resultado:
                self._processar_clique_resultado(evento.pos)
                continue

            if evento.type == pygame.MOUSEWHEEL:
                pos_mouse = pygame.mouse.get_pos()
                if self.area_sequencia.collidepoint(pos_mouse):
                    self.scroll_y -= evento.y * 25
                    self._limitar_scroll()
                continue

            if evento.type == pygame.MOUSEMOTION and self._drag_item is not None:
                dx = abs(evento.pos[0] - self._drag_iniciou_em[0])
                dy = abs(evento.pos[1] - self._drag_iniciou_em[1])
                if dx > 5 or dy > 5:
                    self._drag_ativo = True
                self._drag_pos = evento.pos
                continue

            if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and self._drag_item is not None:
                pos_mouse = evento.pos
                if self._drag_ativo:
                    indice_destino = self._calcular_indice_insercao(pos_mouse)
                    if indice_destino is not None and indice_destino != self._drag_indice_origem:
                        item = self.lista_pecas.pop(self._drag_indice_origem)
                        if indice_destino > self._drag_indice_origem:
                            indice_destino -= 1
                        self.lista_pecas.insert(indice_destino, item)
                else:
                    if self._remover_item_sequencia(pos_mouse):
                        self.som_clique.play()
                self._drag_item = None
                self._drag_indice_origem = None
                self._drag_ativo = False
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
                            self.som_clique.play()
                            self._fechar_loop()
                        elif self.botao_reset.checar_clique(pos_mouse):
                            self._reset_completo()

                else:
                    if self.area_sequencia.collidepoint(pos_mouse):
                        for item in getattr(self, "_hitboxes_sequencia", []):
                            if item["rect"].collidepoint(pos_mouse) and item["tipo"] in ("bloco_solto", "loop_inteiro"):
                                self._drag_item = self.lista_pecas[item["indice_peca"]]
                                self._drag_indice_origem = item["indice_peca"]
                                self._drag_pos = pos_mouse
                                self._drag_iniciou_em = pos_mouse
                                self._drag_ativo = False
                                break
                        else:
                            if self._remover_item_sequencia(pos_mouse):
                                self.som_clique.play()
                        continue

                    clicou_bloco = False
                    for nome, bloco in self.blocos_paleta.items():
                        if bloco.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self.lista_pecas.append(bloco.clonar_bloco())
                            clicou_bloco = True
                            break

                    if not clicou_bloco:
                        blocos_fase = self.dados.get("blocos_disponiveis", [])
                        if "repetir" in blocos_fase and self.bloco_repetir_paleta.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self._iniciar_loop()
                        elif self.botao_deploy.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self.personagem.iniciar_programacao(self.lista_pecas, self.pontuacao)
                        elif self.botao_reset.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self._reset_completo()
                        elif self.botao_sair.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self.acao_final = "menu_principal"
                            self.rodando = False
                        elif self.botao_menos.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self.n_repeticoes = max(1, self.n_repeticoes - 1)
                            self.bloco_repetir_paleta.n = self.n_repeticoes
                        elif self.botao_mais.checar_clique(pos_mouse):
                            self.som_clique.play()
                            self.n_repeticoes = min(9, self.n_repeticoes + 1)
                            self.bloco_repetir_paleta.n = self.n_repeticoes

    def atualizar(self):
        if self.estado_resultado:
            return
        self.personagem.atualizar_movimento(self.matriz)
        if self.personagem.chegou_no_objetivo:
            if self.estado_resultado is None:
                self.som_passou_fase.play()
            self.estado_resultado = "vitoria"

        elif self.personagem.vidas <= 0:
            if self.estado_resultado is None:
                self.som_game_over.play()
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
        self.personagem._pontuacao = self.pontuacao
        self._drag_iniciou_em = (0, 0)
        self._drag_ativo = False

    def _processar_clique_resultado(self, pos_mouse):
        self.som_clique.play()
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
        # Limpa a sequência de comandos e reabilita todos os blocos da paleta
        self.lista_pecas.clear()
        for bloco in self.blocos_paleta.values():
            if bloco:
                bloco.clicado = False
                bloco.cor = CORES["AZUL_MARINHO"]

        # O restante do reset do bloco de repetir e pontuação continua igual:
        self.modo_loop = False
        self.loop_ativo = None
        self.bloco_repetir_paleta.clicado = False
        self.bloco_repetir_paleta.cor = (220, 130, 0)
        self.pontuacao.resetar()
        self.personagem._pontuacao = self.pontuacao

    def _remover_item_sequencia(self, pos_mouse):
        # Percorre os itens clicáveis na ordem em que foram desenhados
        # (blocos internos de um loop vêm antes da caixa do loop, então têm prioridade)
        for item in getattr(self, "_hitboxes_sequencia", []):
            if not item["rect"].collidepoint(pos_mouse):
                continue

            if item["tipo"] == "comando_no_loop":
                # Remove só aquele bloco específico de dentro do loop
                peca_pai = item["peca_pai"]
                indice = item["indice_no_loop"]
                if 0 <= indice < len(peca_pai.comandos):
                    bloco_removido = peca_pai.comandos.pop(indice)
                    self._reabilitar_bloco_na_paleta(bloco_removido)
                return True

            if item["tipo"] == "loop_inteiro":
                # Remove o loop inteiro, reabilitando todos os blocos que estavam dentro dele
                indice = item["indice_peca"]
                peca = self.lista_pecas[indice]
                for bloco_interno in peca.comandos:
                    self._reabilitar_bloco_na_paleta(bloco_interno)
                self.lista_pecas.pop(indice)
                return True

            if item["tipo"] == "bloco_solto":
                # Remove o bloco solto da sequência principal
                indice = item["indice_peca"]
                bloco_removido = self.lista_pecas.pop(indice)
                self._reabilitar_bloco_na_paleta(bloco_removido)
                return True

        return False

    def _reabilitar_bloco_na_paleta(self, bloco_removido):
        # Ao remover um bloco da sequência, o bloco ORIGINAL correspondente na paleta
        tipo_removido = getattr(bloco_removido, "tipo", None)
        if tipo_removido is None:
            return
        for bloco_paleta in self.blocos_paleta.values():
            if getattr(bloco_paleta, "tipo", None) == tipo_removido and bloco_paleta.clicado:
                bloco_paleta.clicado = False
                bloco_paleta.cor = CORES["AZUL_MARINHO"]
                break

    def _desenhar_linha_translucida(self, y):
        surf = pygame.Surface((LARGURA_TELA - self.PAINEL_X, 2), pygame.SRCALPHA)
        surf.fill((255, 255, 255, 60))
        self.tela.blit(surf, (self.PAINEL_X, y))

    def _desenhar_destaque_sair(self, rect_botao):
        
        destaque = rect_botao.inflate(6, 6)
        pygame.draw.rect(self.tela, (255, 255, 255), destaque, 2, border_radius=6)

    def _desenhar_icone_e_texto_centralizado(self, rect_botao, icone, texto):
        
        espaco_entre = 8

        label = self._fonte_botoes_acoes.render(texto, True, (255, 255, 255))

        largura_total = icone.get_width() + espaco_entre + label.get_width()
        x_inicial = rect_botao.centerx - largura_total // 2

        icone_rect = icone.get_rect(midleft=(x_inicial, rect_botao.centery))
        self.tela.blit(icone, icone_rect)

        label_rect = label.get_rect(midleft=(icone_rect.right + espaco_entre, rect_botao.centery))
        self.tela.blit(label, label_rect)

    def _desenhar_texto_botao_acao(self, rect_botao, texto):
      
        label = self._fonte_botoes_acoes.render(texto, True, (255, 255, 255))
        label_rect = label.get_rect(center=rect_botao.center)
        self.tela.blit(label, label_rect)

    def _desenhar_divisor_acoes(self, y):
        # Linha pontilhada horizontal, separando grupos de botões na caixa de ações
        x_inicio = self.area_acoes.x + 15
        x_fim = self.area_acoes.right - 15
        x = x_inicio
        while x < x_fim:
            pygame.draw.line(self.tela, (120, 140, 200), (x, y), (x + 6, y), 2)
            x += 12

    def _limitar_scroll(self):
        if self.scroll_y < 0:
            self.scroll_y = 0
        
        maximo = max(0, self.altura_conteudo - (self.area_sequencia.height - 70))
        if self.scroll_y > maximo:
            self.scroll_y = maximo

    def _desenhar_bloco_repetir_na_sequencia(self, peca, x, y, largura_bloco, indice_peca, em_construcao, hitboxes):
        # Desenha uma caixa de loop (laranja) com seus comandos dentro.
        # Se em_construcao=True, usa cores translúcidas (loop ainda sendo montado).
        altura = 70 + len(peca.comandos) * 45

        caixa = pygame.Rect(x, y, largura_bloco, altura)

        if em_construcao:
            cor_fundo = (180, 100, 0, 110)
            cor_borda = (255, 200, 0, 130)
        else:
            cor_fundo = (180, 100, 0, 255)
            cor_borda = (255, 200, 0, 255)

        superficie_loop = pygame.Surface((largura_bloco, altura), pygame.SRCALPHA)
        pygame.draw.rect(superficie_loop, cor_fundo, (0, 0, largura_bloco, altura), border_radius=10)
        pygame.draw.rect(superficie_loop, cor_borda, (0, 0, largura_bloco, altura), 3, border_radius=10)
        self.tela.blit(superficie_loop, (x, y))

        cor_texto = (255, 255, 255, 160) if em_construcao else (255, 255, 255, 255)
        texto_surf = pygame.Surface((140, 20), pygame.SRCALPHA)
        texto_render = self._fonte_ui.render(f"Rep x{peca.n}", True, (255, 255, 255))
        texto_surf.blit(texto_render, (0, 0))
        if em_construcao:
            texto_surf.set_alpha(160)
        self.tela.blit(texto_surf, (x + 10, y + 10))

        y_loop = y + 45

        for indice_cmd, cmd in enumerate(peca.comandos):
            cmd.rect.x = x + 35
            cmd.rect.y = y_loop

            if em_construcao:
                # Desenha o bloco numa superfície separada para poder aplicar transparência
                bloco_surf = pygame.Surface(cmd.rect.size, pygame.SRCALPHA)
                rect_original = cmd.rect.copy()
                cmd.rect.topleft = (0, 0)
                cmd.desenhar(bloco_surf)
                cmd.rect = rect_original
                bloco_surf.set_alpha(140)
                self.tela.blit(bloco_surf, cmd.rect.topleft)
            else:
                cmd.desenhar(self.tela)

            if hitboxes is not None:
                hitboxes.append({
                    "rect": cmd.rect.copy(),
                    "tipo": "comando_no_loop",
                    "peca_pai": peca,
                    "indice_no_loop": indice_cmd,
                })

            y_loop += 35

        if hitboxes is not None:
            hitboxes.append({
                "rect": caixa.copy(),
                "tipo": "loop_inteiro",
                "indice_peca": indice_peca,
            })

        return altura

    def _desenhar_fila_comandos(self):
        inicio_x = self.area_sequencia.x + 30
        inicio_y = self.area_sequencia.y + 60

        largura_bloco = 160
        altura_bloco_simples = 45
        espacamento_y = 15

        x = inicio_x
        # Desloca o início pelo valor do scroll (sobe o conteúdo conforme rola pra baixo)
        y = inicio_y - self.scroll_y

       
        area_recorte = pygame.Rect(
            self.area_sequencia.x + 3,
            self.area_sequencia.y + 50,
            self.area_sequencia.width - 6,
            self.area_sequencia.height - 56
        )
        clip_anterior = self.tela.get_clip()
        self.tela.set_clip(area_recorte)

        
        self._hitboxes_sequencia = []

        for indice_peca, peca in enumerate(self.lista_pecas):

            if peca is None:
                continue

            if getattr(peca, "tipo", None) == "repetir":
                if indice_peca != self._drag_indice_origem or not self._drag_ativo:
                    altura = self._desenhar_bloco_repetir_na_sequencia(
                        peca, x, y, largura_bloco, indice_peca,
                        em_construcao=False,
                        hitboxes=self._hitboxes_sequencia
                    )
                else:
                    altura = 70 + len(peca.comandos) * 45
                y += altura + espacamento_y

            else:
                peca.rect.topleft = (x, y)
                if indice_peca != self._drag_indice_origem or not self._drag_ativo:
                    peca.desenhar(self.tela)

                # Registra o bloco solto (fora de qualquer loop)
                self._hitboxes_sequencia.append({
                    "rect": peca.rect.copy(),
                    "tipo": "bloco_solto",
                    "indice_peca": indice_peca,
                })

    
                y += altura_bloco_simples + espacamento_y

        
        if self.modo_loop and self.loop_ativo is not None:
            self._desenhar_bloco_repetir_na_sequencia(
                self.loop_ativo, x, y, largura_bloco, indice_peca=None,
                em_construcao=True,
                hitboxes=None
            )
            y += 70 + len(self.loop_ativo.comandos) * 45 + espacamento_y

        self.tela.set_clip(clip_anterior)

        self.altura_conteudo = (y + self.scroll_y) - inicio_y

       
        self.tela.set_clip(clip_anterior)

        
        self.altura_conteudo = (y + self.scroll_y) - inicio_y


    def desenhar(self):
        self.tela.fill(CORES["FUNDO"])
        pygame.draw.rect(self.tela,CORES["FUNDO"],(self.PAINEL_X,0,LARGURA_TELA-self.PAINEL_X,ALTURA_TELA))
        for area in [
            self.area_como_jogar,
            self.area_blocos,
            self.area_sequencia,
            self.area_acoes
        ]:

            pygame.draw.rect(self.tela,(25,30,55),area,border_radius=12)

            pygame.draw.rect(self.tela,(120,140,200),area,3,border_radius=12)
        

        # ── Matriz à esquerda ──
        cols = len(self.matriz[0])
        rows = len(self.matriz)

        BORDA = 1
        total_cols = cols + 2 * BORDA
        total_rows = rows + 2 * BORDA

        offset_x = (self.PAINEL_X - total_cols * TAMANHO_CELULA) // 2
        offset_y = (ALTURA_TELA - total_rows * TAMANHO_CELULA) // 2

        # 1. Desenha as paredes externas
        for i in range(total_rows):
            for j in range(total_cols):
                x = offset_x + j * TAMANHO_CELULA
                y = offset_y + i * TAMANHO_CELULA
                sprite_p = self.objeto_matriz._sprite_parede(i, j, total_rows, total_cols)
                if sprite_p:
                    self.tela.blit(sprite_p, (x, y))

        # 2. Desenha o interior (Células e Entidades)
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
      
       
        # ── Painel direito: Renderização Dinâmica de Blocos ──
        for bloco in self.blocos_paleta.values():
            bloco.desenhar(self.tela)

        # Interface do Bloco de Repetição (Apenas se disponível no JSON)
        blocos_fase = self.dados.get("blocos_disponiveis", [])
        if self.bloco_repetir_paleta:
            self.botao_menos.desenhar(self.tela)
            minus_lbl = self._fonte_ui.render("-", True, (255, 255, 255))
            self.tela.blit(minus_lbl, (self.botao_menos.rect.x + 7, self.botao_menos.rect.y + 5))

            self.botao_mais.desenhar(self.tela)
            plus_lbl = self._fonte_ui.render("+", True, (255, 255, 255))
            self.tela.blit(plus_lbl, (self.botao_mais.rect.x + 6, self.botao_mais.rect.y + 5))

            n_lbl = self._fonte_ui.render(str(self.n_repeticoes), True, (255, 255, 255))
            n_rect = n_lbl.get_rect(centerx=(self.botao_menos.rect.right + self.botao_mais.rect.left) // 2,centery=self.botao_menos.rect.centery)
            self.tela.blit(n_lbl, n_rect)

            self.bloco_repetir_paleta.desenhar(self.tela)

            if self.modo_loop:
                self.botao_fechar_loop.desenhar(self.tela)
                fechar_lbl = self._fonte_ui.render("Fechar Loop", True, (255, 255, 255))
                self.tela.blit(fechar_lbl, (
                    self.botao_fechar_loop.rect.x + 20,
                    self.botao_fechar_loop.rect.y + 8,
                ))

        pygame.draw.rect(self.tela,(25,30,55),self.area_sequencia,border_radius=12)

        pygame.draw.rect(self.tela,(120,140,200),self.area_sequencia,3,border_radius=12)
    
        titulo_como_jogar = self._fonte_titulo_painel.render("COMO JOGAR", True, (255,255,255))
        rect_titulo_1 = titulo_como_jogar.get_rect(centerx=self.area_como_jogar.centerx, y=self.area_como_jogar.y + 12)
        self.tela.blit(titulo_como_jogar, rect_titulo_1)

        titulo_sequencia = self._fonte_titulo_painel.render("SEQUÊNCIA DE COMANDOS", True, (255,255,255))
        rect_titulo_2 = titulo_sequencia.get_rect(centerx=self.area_sequencia.centerx, y=self.area_sequencia.y + 12)
        self.tela.blit(titulo_sequencia, rect_titulo_2)

        titulo_acoes = self._fonte_ui.render("AÇÕES", True, (255,255,255))
        rect_titulo_3 = titulo_acoes.get_rect(centerx=self.area_acoes.centerx, y=self.area_acoes.y + 14)
        self.tela.blit(titulo_acoes, rect_titulo_3)

        self.desenhar_como_jogar()
        self._desenhar_fila_comandos()

        
        self.botao_deploy.desenhar(self.tela)
        self.botao_reset.desenhar(self.tela)
        self.botao_sair.desenhar(self.tela)

        self._desenhar_destaque_sair(self.botao_sair.rect)

        self._desenhar_icone_e_texto_centralizado(self.botao_deploy.rect, self._icone_play, "EXECUTAR")
        self._desenhar_icone_e_texto_centralizado(self.botao_reset.rect, self._icone_reset, "RESET")
        self._desenhar_divisor_acoes(self.y_divisor_acoes)
        self._desenhar_texto_botao_acao(self.botao_sair.rect, "SAIR")

        texto = self.fonte.render(f"Pontos: {self.pontuacao.pontos}", True, (255, 255, 255))
        self.tela.blit(texto, (10, 10))

        if self.estado_resultado:
            self._desenhar_tela_resultado()

        if self._drag_item is not None and self._drag_ativo:
            surf = pygame.Surface((self._drag_item.rect.width, self._drag_item.rect.height), pygame.SRCALPHA)
            self._drag_item.rect.topleft = (0, 0)
            self._drag_item.desenhar(surf)
            surf.set_alpha(160)
            x_drag = self._drag_pos[0] - self._drag_item.rect.width // 2
            y_drag = self._drag_pos[1] - self._drag_item.rect.height // 2
            self.tela.blit(surf, (x_drag, y_drag))

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

    def _quebrar_texto_em_linhas(self, texto, fonte, largura_maxima):
        # Quebra um texto corrido em várias linhas, respeitando a largura máxima disponível.
        palavras = texto.split(" ")
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            tentativa = (linha_atual + " " + palavra).strip()
            if fonte.size(tentativa)[0] <= largura_maxima:
                linha_atual = tentativa
            else:
                if linha_atual:
                    linhas.append(linha_atual)
                linha_atual = palavra

        if linha_atual:
            linhas.append(linha_atual)

        return linhas

    def desenhar_como_jogar(self):

        paragrafo = (
            "Utilize os blocos de comando para ajudar Nix chegar "
            "até a estrela. Lembre-se: os ovos coletados dão mais pontos"
        )

        largura_texto = self.area_como_jogar.width - 30
        x_texto = self.area_como_jogar.x + 15
        y = self.area_como_jogar.y + 34

        # ── Parágrafo corrido, com quebra de linha automática ──
        linhas_paragrafo = self._quebrar_texto_em_linhas(paragrafo, self._fonte_como_jogar, largura_texto)

        for linha in linhas_paragrafo:
            if y + 14 > self.area_como_jogar.bottom:
                self.tela.set_clip(None)
                return

            texto = self._fonte_como_jogar.render(linha, True, (255, 255, 255))
            self.tela.blit(texto, (x_texto, y))
            y += 15

        y += 8  


        largura_coluna = largura_texto // 2

        linhas_lista = [
            ("↑", "cima", "↓", "baixo"),
            ("←", "esquerda", "→", "direita"),
        ]

        for seta_1, nome_1, seta_2, nome_2 in linhas_lista:
            if y + 14 > self.area_como_jogar.bottom:
                return

            texto_1 = f"{seta_1} {nome_1}"
            texto_2 = f"{seta_2} {nome_2}"

            usa_seta_1 = any(s in texto_1 for s in ("↑", "↓", "←", "→"))
            fonte_1 = self._fonte_setas_texto if usa_seta_1 else self._fonte_como_jogar
            render_1 = fonte_1.render(texto_1, True, (255, 255, 255))
            self.tela.blit(render_1, (x_texto, y))

            usa_seta_2 = any(s in texto_2 for s in ("↑", "↓", "←", "→"))
            fonte_2 = self._fonte_setas_texto if usa_seta_2 else self._fonte_como_jogar
            render_2 = fonte_2.render(texto_2, True, (255, 255, 255))
            self.tela.blit(render_2, (x_texto + largura_coluna, y))

            y += 16

        y += 8  

        explicacao_loop = "loop = quantidade de vezes que deve repetir o movimento"
        explicacao_arrasta = "Arrastar: reorganiza os blocos | Clicar: apaga o bloco"
        linhas_loop = self._quebrar_texto_em_linhas(explicacao_loop, self._fonte_como_jogar, largura_texto)

        for linha in linhas_loop:
            if y + 14 > self.area_como_jogar.bottom:
                return

            texto = self._fonte_como_jogar.render(linha, True, (255, 255, 255))
            self.tela.blit(texto, (x_texto, y))
            y += 15

        y += 4

        explicacao_arrasta = "Arrastar: reorganiza | Clicar: apaga"
        linhas_arrasta = self._quebrar_texto_em_linhas(explicacao_arrasta, self._fonte_como_jogar, largura_texto)
        for linha in linhas_arrasta:
            if y + 14 > self.area_como_jogar.bottom:
                return
            texto = self._fonte_como_jogar.render(linha, True, (200, 200, 200))
            self.tela.blit(texto, (x_texto, y))
            y += 15
            
        inicio_y = self.area_sequencia.y + 60
        altura_bloco = 45
        espacamento_y = 15
        y = inicio_y - self.scroll_y
        for i in range(len(self.lista_pecas) + 1):
            y += altura_bloco + espacamento_y
        return len(self.lista_pecas)

    def _calcular_indice_insercao(self, pos_mouse):
        inicio_y = self.area_sequencia.y + 60
        altura_bloco = 45
        espacamento_y = 15
        y = inicio_y - self.scroll_y
        for i in range(len(self.lista_pecas) + 1):
            if pos_mouse[1] < y + (altura_bloco + espacamento_y) // 2:
                return i
            y += altura_bloco + espacamento_y
        return len(self.lista_pecas)

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.relogio.tick(FPS)
        return self.acao_final
