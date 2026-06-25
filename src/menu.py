import pygame
from src.configuracao import LARGURA_TELA, ALTURA_TELA, FPS, CORES, resource_path
from src.dados import Data

ESCALA = 3  
FONTE_PIXEL = resource_path("assets/fontes/PressStart2P.ttf")


def carregar_fonte(tamanho):
    try:
        return pygame.font.Font(FONTE_PIXEL, tamanho)
    except Exception:
        return pygame.font.SysFont(None, int(tamanho * 1.6))


class BotaoMenu:
    def __init__(self, x, y, largura, altura, texto, desabilitado=False, tile=None, tamanho_fonte=14):
        self.som_clique = pygame.mixer.Sound(resource_path("assets/sons/clique_botoes.mp3"))
        self.som_clique.set_volume(0.08)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.desabilitado = desabilitado
        self._tile = tile
        self._fonte = carregar_fonte(tamanho_fonte)

    def _desenhar_tile_fundo(self, superficie):
        if not self._tile:
            return
        tw = self._tile.get_width()
        th = self._tile.get_height()
        for oy in range(0, self.rect.height, th):
            for ox in range(0, self.rect.width, tw):
                superficie.blit(self._tile, (self.rect.x + ox, self.rect.y + oy))

    def _desenhar_borda_minecraft(self, superficie, hover):
        r = self.rect
        borda = 2
        if self.desabilitado:
            claro  = (70, 70, 80)
            escuro = (30, 30, 35)
        elif hover:
            claro  = (220, 230, 255)
            escuro = (50, 55, 80)
        else:
            claro  = (150, 160, 200)
            escuro = (30, 32, 50)

        
        pygame.draw.rect(superficie, claro,  (r.x, r.y, r.width, borda))
        
        pygame.draw.rect(superficie, claro,  (r.x, r.y, borda, r.height))
       
        pygame.draw.rect(superficie, escuro, (r.x, r.bottom - borda, r.width, borda))
        
        pygame.draw.rect(superficie, escuro, (r.right - borda, r.y, borda, r.height))

    def desenhar(self, superficie):
        hover = (not self.desabilitado) and self.rect.collidepoint(pygame.mouse.get_pos())

       
        overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        if self.desabilitado:
            overlay.fill((10, 10, 20, 160))
        elif hover:
            overlay.fill((80, 100, 160, 120))
        else:
            overlay.fill((20, 25, 50, 140))

        self._desenhar_tile_fundo(superficie)
        superficie.blit(overlay, self.rect.topleft)
        self._desenhar_borda_minecraft(superficie, hover)

        cor_texto = (100, 105, 120) if self.desabilitado else (255, 255, 255)
        label = self._fonte.render(self.texto, True, cor_texto)
        label_rect = label.get_rect(center=self.rect.center)
        superficie.blit(label, label_rect)

    def checar_clique(self, pos):
        return not self.desabilitado and self.rect.collidepoint(pos)


class Menu:
    def __init__(self, tela, relogio):
        self.tela = tela
        self.relogio = relogio
        self.rodando = True
        self.acao = None
        self._carregar_assets()
        self._criar_botoes()

    def _carregar_assets(self):
        def carregar(caminho, escala=None):
            try:
                img = pygame.image.load(resource_path(caminho)).convert_alpha()
                if escala:
                    img = pygame.transform.scale(img, escala)
                return img
            except Exception:
                return None

        tile_size = 16 * ESCALA
        self._tile_fundo    = carregar("assets/sprites/sprits-jogo-python/fundo_16px.png",  (tile_size, tile_size))
        self._tile_pedra    = carregar("assets/sprites/sprits-jogo-python/pedra_1.png",     (tile_size, tile_size))
        self._pilastra      = carregar("assets/sprites/sprits-jogo-python/paredes/pilastra_inteira.png")
        self._personagem    = carregar("assets/sprites/sprits-jogo-python/personagem1.png", (96, 96))
        self._estrela       = carregar("assets/sprites/sprits-jogo-python/estrela.png",     (40, 40))

        self._fonte_titulo  = carregar_fonte(34)
        self._fonte_sub     = carregar_fonte(14)

    def _criar_botoes(self):
        btn_w, btn_h = 280, 46
        centro_x = LARGURA_TELA // 2
        inicio_y = 280
        gap = 14

        tem_save = Data.existe_save()

        opcoes = [
            ("Novo Jogo", False, "novo_jogo"),
            ("Continuar", not tem_save, "continuar"),
            ("Créditos",  False, "creditos"),
            ("Sair",      False, "sair"),
        ]

        self._botoes = []
        for i, (texto, desabilitado, acao) in enumerate(opcoes):
            x = centro_x - btn_w // 2
            y = inicio_y + i * (btn_h + gap)
            botao = BotaoMenu(x, y, btn_w, btn_h, texto, desabilitado)
            botao._acao = acao
            self._botoes.append(botao)

    def _desenhar_fundo(self):
        self.tela.fill(CORES["FUNDO"])

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
        r_s = surf_s.get_rect(center=(sx, sy))
        r_t = surf_t.get_rect(center=pos_center)
        self.tela.blit(surf_s, r_s)
        self.tela.blit(surf_t, r_t)

    def _desenhar_titulo(self):
        centro_x = LARGURA_TELA // 2

        if self._personagem:
            pr = self._personagem.get_rect(center=(140, 130))
            self.tela.blit(self._personagem, pr)

        if self._estrela:
            er = self._estrela.get_rect(center=(LARGURA_TELA - 130, 130))
            self.tela.blit(self._estrela, er)

        self._texto_pixel(
            self._fonte_titulo,
            "Perdido no Algoritmo",
            (180, 210, 255),
            (20, 25, 60),
            (centro_x, 120),
        )

        
        for x in range(centro_x - 220, centro_x + 220, 4):
            pygame.draw.rect(self.tela, (60, 80, 140), (x, 180, 2, 2))

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.acao = "sair"
                self.rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for botao in self._botoes:
                    if botao.checar_clique(evento.pos):
                        botao.som_clique.play()
                        self.acao = botao._acao
                        if self.acao in ("novo_jogo", "continuar", "sair", "creditos"):
                            self.rodando = False

    def desenhar(self):
        self._desenhar_fundo()
        self._desenhar_pilastras()
        self._desenhar_titulo()
        for botao in self._botoes:
            botao.desenhar(self.tela)
        pygame.display.update()

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.desenhar()
            self.relogio.tick(FPS)
        return self.acao
