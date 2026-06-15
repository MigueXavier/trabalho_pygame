import pygame
from src.configuracao import TAMANHO_CELULA, CORES
from src.item import Item
from src.objetivo import Objetivo


class Personagem:
    def __init__(self, linha_inicio, coluna_inicio):
        self.coluna = coluna_inicio
        self.linha = linha_inicio


        self.linha_inicial = linha_inicio
        self.coluna_inicial = coluna_inicio

        self.executando_comandos = False
        self.indice_comando_atual = 0
        self.direcao_atual = None
        self.tempo_ultimo_passo = 0      # ← novo
        self.delay_entre_passos = 500    # ← meio segundo entre cada passo (ms)
        self.comandos_expandidos = []    # flat list built at deploy time
        self.vidas = 3
        self.chegou_no_objetivo = False

    def desenhar(self, superficie, x, y):
        pygame.draw.circle(superficie, (0, 255, 0), (x, y), 15)

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

        # Só executa o próximo passo se já passou o delay
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
                        matriz_jogo[nova_linha][nova_coluna] = None
                        if self._pontuacao is not None:
                            self._pontuacao.adicionar_pontos()
                            print("Pontuação:", self._pontuacao.pontos)
                    if isinstance(elemento_destino, Objetivo):
                        self.chegou_no_objetivo = True
                    matriz_jogo[self.linha][self.coluna] = None
                    self.linha = nova_linha
                    self.coluna = nova_coluna
                    matriz_jogo[self.linha][self.coluna] = self

            self.indice_comando_atual += 1
            self.tempo_ultimo_passo = agora
        else:
            self.executando_comandos = False

            if not self.chegou_no_objetivo:
                self.vidas -= 1
                print(f"Comandos terminaram! Você não chegou ao objetivo. Vidas restantes: {self.vidas}")

                if self.vidas > 0:
                   
                    matriz_jogo[self.linha][self.coluna] = None
                    
                    self.linha = self.linha_inicial
                    self.coluna = self.coluna_inicial
                   
                    matriz_jogo[self.linha][self.coluna] = self