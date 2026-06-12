import pygame
import sys
import copy
from src.barreira import Barreira
from src.personagem import Personagem

tela = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Teste de Barreira")

personagem = Personagem(2, 1)
barreira1 = Barreira( 50, (255, 0, 0))

# criar matrizes diferentes para fases futuras

class Matriz:
    def __init__(self):
        self.matriz = [
            [barreira1, None, None, None],
            [barreira1, barreira1, None, None],
            [barreira1, personagem, None, None],
            [barreira1, barreira1, barreira1, barreira1]
        ]
 




