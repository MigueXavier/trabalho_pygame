import pygame
from src.configuracao import TAMANHO_CELULA, CORES


class Personagem:
    def __init__(self, linha_inicio, coluna_inicio):
        self.coluna = coluna_inicio
        self.linha = linha_inicio
        self.executando_comandos = False
        self.indice_comando_atual = 0
        self.direcao_atual = None
        self.tempo_ultimo_passo = 0      # ← novo
        self.delay_entre_passos = 500    # ← meio segundo entre cada passo (ms)

    def desenhar(self, superficie, x, y):
        pygame.draw.circle(superficie, (0, 255, 0), (x, y), 15)

    def iniciar_programacao(self):
        self.executando_comandos = True
        self.indice_comando_atual = 0
        self.tempo_ultimo_passo = pygame.time.get_ticks()  # ← marca o tempo inicial

    def atualizar_movimento(self, lista_pecas, matriz_jogo):
        if not self.executando_comandos:
            return

        # Só executa o próximo passo se já passou o delay
        agora = pygame.time.get_ticks()
        if agora - self.tempo_ultimo_passo < self.delay_entre_passos:
            return   # ← ainda não é hora de mover

        if self.indice_comando_atual < len(lista_pecas):
            peca_atual = lista_pecas[self.indice_comando_atual]
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
                if elemento_destino is None or elemento_destino == self:
                    matriz_jogo[self.linha][self.coluna] = None
                    self.linha = nova_linha
                    self.coluna = nova_coluna
                    matriz_jogo[self.linha][self.coluna] = self

            self.indice_comando_atual += 1
            self.tempo_ultimo_passo = agora  # ← atualiza o tempo após cada passo
        else:
            self.executando_comandos = False