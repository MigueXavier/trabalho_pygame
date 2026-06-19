import pygame
from sys import exit
from src.menu import Menu
from src.jogo import Jogo

jogo = Jogo()

if __name__ == "__main__":
    pygame.init()
    tela = jogo.tela
    pygame.display.set_caption("Perdido no Algoritmo")
    relogio = pygame.time.Clock()

    menu = Menu(tela, relogio)
    acao = menu.rodar()

    if acao == "novo_jogo":
        meu_jogo = Jogo()
        meu_jogo.rodar()
    elif acao == "sair":
        pygame.quit()
        exit()

