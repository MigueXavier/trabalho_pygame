import pygame
import sys
import copy
from src.configuracao import *
from src.barreira import Barreira
from src.personagem import Personagem
from src.item import Item
from src.objetivo import Objetivo

tela = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Teste de Barreira")


personagem = Personagem(0, 0)  
barreira1 = Barreira(50, (255, 0, 0))
objetivo = Objetivo()
item1 = Item()     
estrela = Item()  


import pygame
import sys
import copy
from src.configuracao import *
from src.barreira import Barreira
from src.personagem import Personagem
from src.item import Item
from src.objetivo import Objetivo


class Matriz:
    def __init__(self):
      
        self.spritesheet = pygame.image.load("assets/sprites/sprits-jogo-python/dungeon_sheet.png").convert_alpha()
        
        
        self.TAM_SPRITE_BASE = 16 

       
        coordenadas_paredes = {
           
            "canto_topo_esq":  (0, 0, 16, 16),    # Primeira célula do topo esquerdo
            "topo":            (16, 0, 16, 16),   # Bloco do meio do topo
            "canto_topo_dir":  (32, 0, 16, 16),   # Terceira célula do topo (borda direita)
            
            # Linha do Meio (Y = 16)
            "esquerda":        (0, 16, 16, 16),   # Borda esquerda pura
            "direita":         (32, 16, 16, 16),  # Borda direita pura
            
            # Linha de Baixo (Y = 32)
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

        rows = 5  
        cols = 5  
        self.matriz = [
            [personagem, None, None, item1,   None  ],
            [None,       barreira1, None, barreira1, None  ],
            [item1,    barreira1, None, None,  None  ],
            [None,       None,  None, barreira1, objetivo],
            [None,       None,  item1, None,  None  ],
        ]

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