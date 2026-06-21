import pygame
import webbrowser
from src.configuracao import LARGURA_TELA, ALTURA_TELA, FPS, CORES
from src.menu import carregar_fonte, BotaoMenu

LINK_DRIVE = "https://docs.google.com/document/d/1oPYUyG7PTLMurCZRVeUnn1HWvLiTJ0tqD6Mjl2VeP3c/edit?usp=drivesdk"

INTEGRANTES = [
    "Arthur Fernandes Fialho e Silva",
    "Arthur Rodrigues de Macedo",
    "Miguel Xavier dos Santos",
    "Pamela Fernandes Nilo",
    "Túlio Marcus de Oliveira Gonçalves",
]


class Creditos:
    def __init__(self, tela, relogio):
        self.tela = tela
        self.relogio = relogio
        self.rodando = True
        self._carregar_assets()
        self._criar_botoes()

    def _carregar_assets(self):
        def carregar(caminho, escala=None):
            try:
                img = pygame.image.load(caminho).convert_alpha()
                if escala:
                    img = pygame.transform.scale(img, escala)
                return img
            except Exception:
                return None

        self._pilastra   = carregar("assets/sprites/sprits-jogo-python/paredes/pilastra_inteira.png")
        self._estrela    = carregar("assets/sprites/sprits-jogo-python/estrela.png", (28, 28))

        self._fonte_titulo  = carregar_fonte(18)
        self._fonte_secao   = carregar_fonte(8)
        self._fonte_nome    = carregar_fonte(7)
        self._fonte_link    = carregar_fonte(7)

    def _criar_botoes(self):
        cx = LARGURA_TELA // 2
        btn_w, btn_h = 220, 40
        self._btn_voltar = BotaoMenu(cx - btn_w // 2, ALTURA_TELA - 70, btn_w, btn_h, "< Voltar", tamanho_fonte=10)
        self._btn_drive  = BotaoMenu(cx - btn_w // 2, ALTURA_TELA - 120, btn_w, btn_h, "Abrir no Drive", tamanho_fonte=10)

    def _desenhar_pilastras(self):
        if not self._pilastra:
            return
        ph = self._pilastra.get_height()
        pw = self._pilastra.get_width()
        for y in range(0, ALTURA_TELA, ph):
            self.tela.blit(self._pilastra, (0, y))
            self.tela.blit(self._pilastra, (LARGURA_TELA - pw, y))
        pilastra_h = pygame.transform.rotate(self._pilastra, 90)
        bh = pilastra_h.get_height()
        for x in range(0, LARGURA_TELA, pilastra_h.get_width()):
            self.tela.blit(pilastra_h, (x, 0))
            self.tela.blit(pilastra_h, (x, ALTURA_TELA - bh))

    def _texto_pixel(self, fonte, texto, cor, sombra, pos_center):
        sx, sy = pos_center[0] + 3, pos_center[1] + 3
        surf_s = fonte.render(texto, True, sombra)
        surf_t = fonte.render(texto, True, cor)
        self.tela.blit(surf_s, surf_s.get_rect(center=(sx, sy)))
        self.tela.blit(surf_t, surf_t.get_rect(center=pos_center))

    def _desenhar_conteudo(self):
        cx = LARGURA_TELA // 2

        # ── Título ────────────────────────────────────────────────────────────
        self._texto_pixel(self._fonte_titulo, "CREDITOS",
                          (180, 210, 255), (20, 25, 60), (cx, 65))

        # Linha decorativa de pontos
        for x in range(cx - 220, cx + 220, 4):
            pygame.draw.rect(self.tela, (60, 80, 140), (x, 100, 2, 2))

        # ── Seção: Desenvolvido por ───────────────────────────────────────────
        self._texto_pixel(self._fonte_secao, "DESENVOLVIDO POR",
                          (130, 160, 230), (10, 15, 40), (cx, 125))

        for i, nome in enumerate(INTEGRANTES):
            y = 155 + i * 30

            # Estrelinha decorativa
            if self._estrela:
                er = self._estrela.get_rect(center=(cx - 175, y))
                self.tela.blit(self._estrela, er)

            # Sombra + texto do nome
            surf_s = self._fonte_nome.render(nome, True, (20, 25, 60))
            surf_t = self._fonte_nome.render(nome, True, (220, 225, 255))
            self.tela.blit(surf_s, surf_s.get_rect(midleft=(cx - 150, y + 2)))
            self.tela.blit(surf_t, surf_t.get_rect(midleft=(cx - 150, y)))

        # Linha separadora
        sep_y = 320
        for x in range(cx - 220, cx + 220, 4):
            pygame.draw.rect(self.tela, (60, 80, 140), (x, sep_y, 2, 2))

        # ── Infos extras ──────────────────────────────────────────────────────
        infos = [
            ("Linguagem:", "Python 3.10+ / Pygame"),
            ("Ano:",       "2026"),
        ]
        for i, (chave, valor) in enumerate(infos):
            y = sep_y + 20 + i * 22
            sc = self._fonte_link.render(chave, True, (120, 140, 200))
            sv = self._fonte_link.render(valor,  True, (200, 210, 240))
            self.tela.blit(sc, sc.get_rect(midright=(cx - 4, y)))
            self.tela.blit(sv, sv.get_rect(midleft=(cx + 4, y)))

        # ── Aviso do link ─────────────────────────────────────────────────────
        aviso = self._fonte_link.render("Fontes e referencias no Drive:", True, (140, 160, 210))
        self.tela.blit(aviso, aviso.get_rect(center=(cx, sep_y + 74)))

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
                return "sair"
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.rodando = False
                return "menu"
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self._btn_voltar.checar_clique(evento.pos):
                    self._btn_voltar.som_clique.play()
                    self.rodando = False
                    return "menu"
                if self._btn_drive.checar_clique(evento.pos):
                    self._btn_drive.som_clique.play()
                    webbrowser.open(LINK_DRIVE)
        return None

    def desenhar(self):
        self.tela.fill(CORES["FUNDO"])
        self._desenhar_pilastras()
        self._desenhar_conteudo()
        self._btn_drive.desenhar(self.tela)
        self._btn_voltar.desenhar(self.tela)
        pygame.display.update()

    def rodar(self):
        while self.rodando:
            resultado = self.processar_eventos()
            if resultado:
                return resultado
            self.desenhar()
            self.relogio.tick(FPS)
        return "menu"
