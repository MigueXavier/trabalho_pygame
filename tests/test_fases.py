"""Testes de integridade dos arquivos de fase (fases/*.json).

Garantem que cada fase tenha um formato válido para ser carregada pelo
jogo: chaves obrigatórias, mapa retangular, exatamente um ponto de
partida do personagem (código 1) e ao menos um objetivo (código 4).
"""

import json
from pathlib import Path

import pytest

PASTA_FASES = Path(__file__).resolve().parent.parent / "fases"
ARQUIVOS_FASE = sorted(PASTA_FASES.glob("fase_*.json"))


CODIGO_VAZIO = 0
CODIGO_PERSONAGEM = 1
CODIGO_BARREIRA = 2
CODIGO_ITEM = 3
CODIGO_OBJETIVO = 4
CODIGOS_VALIDOS = {CODIGO_VAZIO, CODIGO_PERSONAGEM, CODIGO_BARREIRA, CODIGO_ITEM, CODIGO_OBJETIVO}


def test_existe_pelo_menos_uma_fase():
    assert len(ARQUIVOS_FASE) >= 1, "Nenhum arquivo fases/fase_*.json encontrado"


@pytest.mark.parametrize("caminho_arquivo", ARQUIVOS_FASE, ids=lambda p: p.name)
def test_fase_possui_chaves_obrigatorias(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    for chave in ("fase", "blocos_disponiveis", "mapa"):
        assert chave in dados, f"{caminho_arquivo.name} não possui a chave '{chave}'"


@pytest.mark.parametrize("caminho_arquivo", ARQUIVOS_FASE, ids=lambda p: p.name)
def test_fase_mapa_e_retangular_e_usa_apenas_codigos_validos(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    mapa = dados["mapa"]
    assert len(mapa) > 0, f"{caminho_arquivo.name}: mapa vazio"

    largura_primeira_linha = len(mapa[0])
    for linha in mapa:
        assert len(linha) == largura_primeira_linha, (
            f"{caminho_arquivo.name}: todas as linhas do mapa devem ter o mesmo tamanho"
        )
        for celula in linha:
            assert celula in CODIGOS_VALIDOS, (
                f"{caminho_arquivo.name}: código de célula inválido encontrado: {celula}"
            )


@pytest.mark.parametrize("caminho_arquivo", ARQUIVOS_FASE, ids=lambda p: p.name)
def test_fase_possui_exatamente_um_ponto_de_partida(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    total_personagens = sum(
        1 for linha in dados["mapa"] for celula in linha if celula == CODIGO_PERSONAGEM
    )
    assert total_personagens == 1, (
        f"{caminho_arquivo.name} deve ter exatamente 1 ponto de partida (código {CODIGO_PERSONAGEM}), "
        f"encontrado(s) {total_personagens}"
    )


@pytest.mark.parametrize("caminho_arquivo", ARQUIVOS_FASE, ids=lambda p: p.name)
def test_fase_possui_ao_menos_um_objetivo(caminho_arquivo):
    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    total_objetivos = sum(
        1 for linha in dados["mapa"] for celula in linha if celula == CODIGO_OBJETIVO
    )
    assert total_objetivos >= 1, (
        f"{caminho_arquivo.name} deve ter ao menos 1 objetivo (código {CODIGO_OBJETIVO})"
    )


@pytest.mark.parametrize("caminho_arquivo", ARQUIVOS_FASE, ids=lambda p: p.name)
def test_fase_carrega_corretamente_na_matriz_do_jogo(caminho_arquivo):
    """Garante que o JSON da fase é consumido sem erros pelo motor do jogo."""
    from src.matriz import Matriz

    with open(caminho_arquivo, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    matriz = Matriz(dados)

    assert len(matriz.matriz) == len(dados["mapa"])
    assert len(matriz.matriz[0]) == len(dados["mapa"][0])
