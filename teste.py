import pygame
import sys
from src.configuracao import *
from src.matriz import Matriz
from src.personagem import Personagem

matriz = Matriz().matriz

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    
    

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            x = j * 50 + 30
            y = i * 50 + 30
            if matriz[i][j] is not None:
                if isinstance(matriz[i][j], Personagem):
                 
                    matriz[i][j].desenhar(tela, x + 25, y + 25)
                else:
                   
                    matriz[i][j].desenhar(tela, x, y)
            

    pygame.display.flip()