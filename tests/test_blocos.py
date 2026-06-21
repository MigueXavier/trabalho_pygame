"""Testes para src.blocos (blocos de comando da sequência)."""

from src.blocos import (
    BlocoBaixo,
    BlocoCima,
    BlocoDireita,
    BlocoEsquerda,
    BlocoRepetir,
)


def test_cada_bloco_direcional_possui_o_tipo_correto():
    assert BlocoDireita(0, 0).tipo == "direita"
    assert BlocoEsquerda(0, 0).tipo == "esquerda"
    assert BlocoCima(0, 0).tipo == "cima"
    assert BlocoBaixo(0, 0).tipo == "baixo"


def test_bloco_repetir_guarda_quantidade_e_lista_de_comandos_vazia():
    bloco = BlocoRepetir(0, 0, n=4)

    assert bloco.tipo == "repetir"
    assert bloco.n == 4
    assert bloco.comandos == []


def test_acao_marca_bloco_como_clicado_uma_unica_vez():
    bloco = BlocoDireita(0, 0)
    assert bloco.clicado is False

    bloco.acao()
    cor_apos_primeiro_clique = bloco.cor
    assert bloco.clicado is True

    # uma segunda chamada não deve alterar o estado novamente
    bloco.acao()
    assert bloco.cor == cor_apos_primeiro_clique


def test_clonar_bloco_repetir_gera_copia_independente():
    original = BlocoRepetir(0, 0, n=2)
    original.comandos.append(BlocoDireita(0, 0))

    clone = original.clonar_bloco()

    # é uma cópia (não a mesma instância)
    assert clone is not original
    assert clone.comandos is not original.comandos

    # alterar o clone não deve afetar o original
    clone.comandos.append(BlocoEsquerda(0, 0))
    assert len(clone.comandos) == 2
    assert len(original.comandos) == 1


def test_checar_clique_detecta_ponto_dentro_do_retangulo():
    bloco = BlocoDireita(10, 10)
    centro = bloco.rect.center

    assert bloco.checar_clique(centro) is True
    assert bloco.checar_clique((-1000, -1000)) is False
