import pygame
import sys
import copy
from src.barreira import Barreira
from src.personagem import Personagem
from src.item import Item
from src.objetivo import Objetivo

tela = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Teste de Barreira")


personagem = Personagem(1, 1)  
barreira1 = Barreira(50, (255, 0, 0))
objetivo = Objetivo(20, (160, 32, 240))
item1 = Item()     
estrela = Item()    

class Matriz:
    def __init__(self):

        self.matriz = [
           
            [barreira1, barreira1, barreira1, barreira1, barreira1, barreira1, barreira1],
            
            
            [barreira1, personagem, None, None, item1, None, barreira1],
            
           
            [barreira1, None, barreira1, None, barreira1, None, barreira1],
          
            [barreira1, estrela, barreira1, None, None, None, barreira1],
            
           
            [barreira1, None, None, None, barreira1, objetivo, barreira1],
            
            
            [barreira1, None, None, estrela, None, None, barreira1],
            
           
            [barreira1, barreira1, barreira1, barreira1, barreira1, barreira1, barreira1]
        ]