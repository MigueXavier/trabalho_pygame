"""Testes para src.matriz.Matriz (construção do labirinto a partir do JSON da fase)."""

from src.barreira import Barreira
from src.item import Item
from src.matriz import Matriz
from src.objetivo import Objetivo
from src.personagem import Personagem


def test_matriz_sem_dados_de_fase_usa_fallback_5x5_vazio():
    matriz = Matriz()

    assert len(matriz.matriz) == 5
    assert all(len(linha) == 5 for linha in matriz.matriz)
    assert all(celula is None for linha in matriz.matriz for celula in linha)


def test_construir_mapa_converte_codigos_numericos_nos_objetos_corretos():
    mapa_numerico = [
        [1, 0, 2],
        [3, 4, 0],
    ]

    matriz = Matriz({"mapa": mapa_numerico})

    assert isinstance(matriz.matriz[0][0], Personagem)
    assert matriz.matriz[0][1] is None
    assert isinstance(matriz.matriz[0][2], Barreira)
    assert isinstance(matriz.matriz[1][0], Item)
    assert isinstance(matriz.matriz[1][1], Objetivo)
    assert matriz.matriz[1][2] is None


def test_construir_mapa_preserva_dimensoes_do_mapa_original():
    mapa_numerico = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 4],
    ]

    matriz = Matriz({"mapa": mapa_numerico})

    assert len(matriz.matriz) == 3
    assert all(len(linha) == 4 for linha in matriz.matriz)
