import pygame
import os
from src.configuracao import LARGURA_TELA  

class Vidas:
    def __init__(self, vidas_iniciais=3):
        self.vidas_max = vidas_iniciais
        self.vidas_atuaes = vidas_iniciais
        
        
        self.tamanho_sprite = (30, 30)
        
       
        caminho_asset = "assets/sprites/sprits-jogo-python/vida.png"
        
        try:
          
            self.imagem_coracao = pygame.image.load(caminho_asset).convert_alpha()
          
            self.imagem_coracao = pygame.transform.scale(self.imagem_coracao, self.tamanho_sprite)
        except pygame.error:
           
            print(f"Erro: Não foi possível carregar o asset em {caminho_asset}. Usando fallback de superfície pura.")
            self.imagem_coracao = pygame.Surface(self.tamanho_sprite, pygame.SRCALPHA)
            pygame.draw.polygon(self.imagem_coracao, (255, 0, 0), [(15, 5), (25, 15), (15, 28), (5, 15)])

    def perder_vida(self):
        if self.vidas_atuaes > 0:
            self.vidas_atuaes -= 1

    def resetar(self):
        self.vidas_atuaes = self.vidas_max

    def desenhar(self, tela, vidas_atuaes):
        self.vidas_atuaes = vidas_atuaes
        
       
        margem_esquerda = 10
        margem_superior = 90  
        espacamento = 10
        
        for i in range(self.vidas_atuaes):
         
            x = margem_esquerda + i * (self.tamanho_sprite[0] + espacamento)
            y = margem_superior
            
            tela.blit(self.imagem_coracao, (x, y))