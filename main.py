import pygame
from sys import exit
from src.menu import Menu
from src.jogo import Jogo
from src.creditos import Creditos
from src.dados import Data, dados_padrao
from src.configuracao import *

if __name__ == "__main__":
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Perdido no Algoritmo")
    relogio = pygame.time.Clock()

    executando = True
    while executando:
        menu = Menu(tela, relogio)
        acao = menu.rodar()

        if acao == "sair":
            executando = False

        elif acao == "novo_jogo":
            Data.salvar_dados(dados_padrao)
            meu_jogo = Jogo()
            resultado = meu_jogo.rodar()
            if resultado == "sair":
                executando = False

        elif acao == "continuar":
            meu_jogo = Jogo()
            resultado = meu_jogo.rodar()
            if resultado == "sair":
                executando = False

        elif acao == "creditos":
            creditos = Creditos(tela, relogio)
            resultado = creditos.rodar()
            if resultado == "sair":
                executando = False

    pygame.quit()
    exit()
