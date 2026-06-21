"""Testes para src.pontuacao.Pontuacao."""

from src.pontuacao import Pontuacao


def test_pontuacao_inicia_zerada():
    pontuacao = Pontuacao()
    assert pontuacao.pontos == 0


def test_adicionar_pontos_soma_dez_por_chamada():
    pontuacao = Pontuacao()
    pontuacao.adicionar_pontos()
    assert pontuacao.pontos == 10

    pontuacao.adicionar_pontos()
    pontuacao.adicionar_pontos()
    assert pontuacao.pontos == 30


def test_resetar_zera_pontuacao_acumulada():
    pontuacao = Pontuacao()
    pontuacao.adicionar_pontos()
    pontuacao.adicionar_pontos()

    pontuacao.resetar()

    assert pontuacao.pontos == 0
