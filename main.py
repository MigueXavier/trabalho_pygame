import pygame
from sys import exit
from src.menu import Menu
from src.jogo import Jogo

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sons/musica_fundo.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    tela = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption("Perdido no Algoritmo")
    relogio = pygame.time.Clock()

    executando = True
    while executando:
        menu = Menu(tela, relogio)
        acao = menu.rodar()

        if acao == "sair" or acao is None:
            executando = False
        elif acao == "novo_jogo":
            fase = 1
            while True:
                meu_jogo = Jogo(fase)
                resultado = meu_jogo.rodar()
                if resultado == "proxima_fase":
                    fase += 1
                elif resultado == "repetir_fase":
                    pass
                elif resultado == "menu_principal":
                    break
                else:
                    executando = False
                    break

    pygame.quit()
    exit()
