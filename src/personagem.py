import pygame
import random
from src.configuracao import TAMANHO_CELULA, CORES, VIDAS_MAXIMAS
from src.item import Item
from src.objetivo import Objetivo


class Personagem:
    def __init__(self, linha_inicio, coluna_inicio):
        self.coluna = coluna_inicio
        self.linha = linha_inicio

        self.sprite = pygame.image.load("assets/sprites/sprits-jogo-python/personagem1.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (TAMANHO_CELULA, TAMANHO_CELULA))

        self.sons_passo = [
            pygame.mixer.Sound("assets/sons/step_1.mp3"),
            pygame.mixer.Sound("assets/sons/step_2.mp3"),
            pygame.mixer.Sound("assets/sons/step_3.mp3")
        ]

        for som in self.sons_passo:
            som.set_volume(0.05)

        self.som_coleta = pygame.mixer.Sound("assets/sons/coleta_itens.mp3")
        self.som_coleta.set_volume(0.15)

        self.som_bater = pygame.mixer.Sound("assets/sons/bater_caixa.mp3")
        self.som_bater.set_volume(0.10)

        self.som_perder_vida = pygame.mixer.Sound("assets/sons/perder_vida.mp3")
        self.som_perder_vida.set_volume(0.15)


        self.linha_inicial = linha_inicio
        self.coluna_inicial = coluna_inicio

        self.executando_comandos = False
        self.indice_comando_atual = 0
        self.direcao_atual = None
        self.tempo_ultimo_passo = 0
        self.delay_entre_passos = 500    # meio segundo entre cada passo (ms)
        self.comandos_expandidos = []    # flat list built at deploy time
        self.vidas = VIDAS_MAXIMAS
        self.chegou_no_objetivo = False

    def desenhar(self, superficie, x, y):
         rect = self.sprite.get_rect(center=(x, y))
         superficie.blit(self.sprite, rect)

    def iniciar_programacao(self, lista_pecas, pontuacao=None):
        self.executando_comandos = True
        self.indice_comando_atual = 0
        self.tempo_ultimo_passo = pygame.time.get_ticks()
        self.comandos_expandidos = self._expandir_lista(lista_pecas)
        self._pontuacao = pontuacao

    def _expandir_lista(self, lista):
        """Flatten BlocoRepetir containers into a sequential command list."""
        from src.blocos import BlocoRepetir
        expandida = []
        for peca in lista:
            if isinstance(peca, BlocoRepetir):
                for _ in range(peca.n):
                    expandida.extend(peca.comandos)
            else:
                expandida.append(peca)
        return expandida

    def atualizar_movimento(self, matriz_jogo):
        if not self.executando_comandos:
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_passo < self.delay_entre_passos:
            return

        if self.indice_comando_atual < len(self.comandos_expandidos):
            peca_atual = self.comandos_expandidos[self.indice_comando_atual]
            direcao = peca_atual.tipo

            nova_coluna = self.coluna
            nova_linha = self.linha

            if direcao == "esquerda":
                nova_coluna -= 1
            elif direcao == "direita":
                nova_coluna += 1
            elif direcao == "cima":
                nova_linha -= 1
            elif direcao == "baixo":
                nova_linha += 1

            if 0 <= nova_linha < len(matriz_jogo) and 0 <= nova_coluna < len(matriz_jogo[0]):
                elemento_destino = matriz_jogo[nova_linha][nova_coluna]
                if elemento_destino is None or elemento_destino == self or isinstance(elemento_destino, Item) or isinstance(elemento_destino, Objetivo):
                    if isinstance(elemento_destino, Item):
                        self.som_coleta.play()
                        matriz_jogo[nova_linha][nova_coluna] = None
                        if self._pontuacao is not None:
                            self._pontuacao.adicionar_pontos()
                            print("Pontuação:", self._pontuacao.pontos)
                    if isinstance(elemento_destino, Objetivo):
                        self.chegou_no_objetivo = True
                    matriz_jogo[self.linha][self.coluna] = None
                    self.linha = nova_linha
                    self.coluna = nova_coluna
                    random.choice(self.sons_passo).play()
                    matriz_jogo[self.linha][self.coluna] = self
                else:
                    self.som_bater.play()
            self.indice_comando_atual += 1
            self.tempo_ultimo_passo = agora
        else:
            self.executando_comandos = False

            if not self.chegou_no_objetivo:
                self.vidas -= 1
                self.som_perder_vida.play()
                print(f"Comandos terminaram! Você não chegou ao objetivo. Vidas restantes: {self.vidas}")

                if self.vidas > 0:
                   
                    matriz_jogo[self.linha][self.coluna] = None
                    
                    self.linha = self.linha_inicial
                    self.coluna = self.coluna_inicial
                   
                    matriz_jogo[self.linha][self.coluna] = self