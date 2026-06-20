import pygame

class BotaoMenu:
    def __init__(self, rect, texto, acao):
        self.rect = rect
        self.texto = texto
        self.acao = acao

    def desenhar(self, tela, fonte):
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        cor = (75, 105, 180) if hover else (45, 65, 125)
        
        pygame.draw.rect(tela, cor, self.rect)
        pygame.draw.rect(tela, (220, 230, 255), self.rect, 2)
        
        txt_surf = fonte.render(self.texto, True, (255, 255, 255))
        tela.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

class MenuBase:
    def __init__(self, titulo, cor_titulo):
        self.titulo = titulo
        self.cor_titulo = cor_titulo
        self.botoes = []
        self.painel_rect = pygame.Rect(390, 130, 420, 350)

    def checar_clique(self, pos_mouse):
        for botao in self.botoes:
            if botao.rect.collidepoint(pos_mouse):
                return botao.acao
        return None

    def desenhar(self, tela, fonte_titulo, fonte_botoes):
       
        sobreposicao = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        sobreposicao.fill((0, 0, 0, 185))
        tela.blit(sobreposicao, (0, 0))
        
     
        pygame.draw.rect(tela, (25, 30, 55), self.painel_rect)
        pygame.draw.rect(tela, (170, 190, 255), self.painel_rect, 3)
        
        
        tit_surf = fonte_titulo.render(self.titulo, True, self.cor_titulo)
        tela.blit(tit_surf, tit_surf.get_rect(center=(tela.get_width() // 2, 195)))
        
        
        for botao in self.botoes:
            botao.desenhar(tela, fonte_botoes)

class MenuResultado(MenuBase):
    def __init__(self, tipo_resultado):
        if tipo_resultado == "vitoria":
            super().__init__("RODOU LISO!", (80, 230, 130))
            self.botoes = [
                BotaoMenu(pygame.Rect(480, 285, 240, 44), "Próxima Fase", "proxima_fase"),
                BotaoMenu(pygame.Rect(480, 343, 240, 44), "Repetir Fase", "repetir_fase"),
                BotaoMenu(pygame.Rect(480, 401, 240, 44), "Menu Principal", "menu_principal")
            ]
        else:
            super().__init__("GAME OVER!", (240, 90, 90))
            self.botoes = [
                BotaoMenu(pygame.Rect(480, 310, 240, 44), "Tentar Novamente", "repetir_fase"),
                BotaoMenu(pygame.Rect(480, 368, 240, 44), "Menu Principal", "menu_principal")
            ]