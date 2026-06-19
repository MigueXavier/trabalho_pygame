import pygame
import sys
import copy
from src.configuracao import *
from src.barreira import Barreira
from src.personagem import Personagem
from src.item import Item
from src.objetivo import Objetivo

class Matriz:
    def __init__(self, dados_fase=None):
        # 1. Carregamento Gráfico Existente
        self.spritesheet = pygame.image.load("assets/sprites/sprits-jogo-python/dungeon_sheet.png").convert_alpha()
        self.TAM_SPRITE_BASE = 16 

        coordenadas_paredes = {
            "canto_topo_esq":  (0, 0, 16, 16),    # Primeira célula do topo esquerdo
            "topo":            (16, 0, 16, 16),   # Bloco do meio do topo
            "canto_topo_dir":  (32, 0, 16, 16),   # Terceira célula do topo (borda direita)
            "esquerda":        (0, 16, 16, 16),   # Borda esquerda pura
            "direita":         (32, 16, 16, 16),  # Borda direita pura
            "canto_baixo_esq": (0, 32, 16, 16),   # Quina inferior esquerda
            "baixo":           (16, 32, 16, 16),  # Bloco do meio de baixo
            "canto_baixo_dir": (32, 32, 16, 16),  # Quina inferior direita
        }
        
        self.sprites_parede = {}
        for nome, coord in coordenadas_paredes.items():
            sub_surface = self.spritesheet.subsurface(pygame.Rect(coord))
            self.sprites_parede[nome] = pygame.transform.scale(sub_surface, (TAMANHO_CELULA, TAMANHO_CELULA))

        self.fundo = pygame.image.load("assets/sprites/sprits-jogo-python/fundo_16px.png").convert()
        self.fundo = pygame.transform.scale(self.fundo, (TAMANHO_CELULA, TAMANHO_CELULA))

        # 2. Atributo principal esperado pelo seu jogo.py
        self.matriz = []

        # Constrói o mapa dinamicamente se os dados do JSON existirem
        if dados_fase and "mapa" in dados_fase:
            self.construir_mapa(dados_fase["mapa"])
        else:
            # Fallback seguro para uma matriz vazia 5x5 caso o arquivo falhe
            self.matriz = [[None for _ in range(5)] for _ in range(5)]

    def construir_mapa(self, mapa_numerico):
        """Converte a matriz numérica do JSON em instâncias de objetos Pygame."""
        self.matriz = []
        
        for linha in mapa_numerico:
            nova_linha = []
            for celula in linha:
                if celula == 1:
                    nova_linha.append(Personagem(0, 0))
                    
                elif celula == 2:
                    # Instancia uma barreira passando os argumentos que você já usa
                    nova_linha.append(Barreira(50, (255, 0, 0)))
                    
                elif celula == 3:
                    nova_linha.append(Item())
                    
                elif celula == 4:
                    nova_linha.append(Objetivo())
                    
                else:
                    nova_linha.append(None) # 0 = None
            self.matriz.append(nova_linha)

    def _sprite_parede(self, i, j, rows, cols):
        topo = i == 0
        baixo = i == rows - 1
        esq = j == 0
        dir_ = j == cols - 1

        if topo and esq:   return self.sprites_parede["canto_topo_esq"]
        if topo and dir_:  return self.sprites_parede["canto_topo_dir"]
        if baixo and esq:  return self.sprites_parede["canto_baixo_esq"]
        if baixo and dir_: return self.sprites_parede["canto_baixo_dir"]
        if topo:           return self.sprites_parede["topo"]
        if baixo:          return self.sprites_parede["baixo"]
        if esq:            return self.sprites_parede["esquerda"]
        if dir_:           return self.sprites_parede["direita"]
        return None