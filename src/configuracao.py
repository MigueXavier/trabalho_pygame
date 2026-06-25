import sys
import os

def resource_path(caminho_relativo):
    """Resolve o caminho de um asset, funcionando tanto em desenvolvimento
    quanto dentro de um executável gerado pelo PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base, caminho_relativo)

LARGURA_TELA = 1200
ALTURA_TELA  = 600
FPS          = 60
TITULO       = "Perdido no Algoritmo"

TAMANHO_CELULA = 48   # px por célula da grade
margem = 15
PROP_COMO_JOGAR = 0.24
PROP_BLOCOS = 0.20
PROP_SEQUENCIA = 0.47

CORES = {
    "FUNDO":        (15,  15,  30),
    "COR_LINHA":    (50, 50, 50),
    "VERDE":        (0, 200, 0),
    "VERDE_ESCURO": (0, 100, 0),
    "VERMELHO":     (200, 0, 0),
    "VERMELHO_ESCURO": (100, 0, 0),
    "ROXO":         (200, 0, 200),
    "ROXO_ESCURO": (100, 0, 100),
    "CIANO":         (0, 200, 200),
    "CIANO_ESCURO": (0, 100, 100),
    "CINZA":         (137, 137, 137),
    "AZUL":          (0, 0, 200),
    "AMARELO":       (200, 200, 0),
    "AZUL_MARINHO": (67, 144, 176),
    "AZUL_MARINHO_ESCURO": (35, 77, 88),
    "VERMELHO_VIDA": (220, 40, 40),
    "CINZA_ESCURO": (60, 60, 70)
}

ESTADO_MENU      = "menu"
ESTADO_FASE      = "fase"
ESTADO_PAUSA     = "pausa"
ESTADO_GAME_OVER = "game_over"
ESTADO_VITORIA   = "vitoria"

BLOCO_IF  = "IF"
BLOCO_FOR = "FOR"
BLOCO_AND = "AND"
BLOCO_OR  = "OR"

TIPOS_BLOCOS = [BLOCO_IF, BLOCO_FOR, BLOCO_AND, BLOCO_OR]

MAX_BLOCOS_PILHA = 10

TOTAL_FASES = 3

VIDAS_MAXIMAS = 3