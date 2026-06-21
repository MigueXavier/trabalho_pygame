"""Testes para src.personagem.Personagem (movimentação, colisão, coleta e vidas).

O delay de animação entre passos (`delay_entre_passos`) é contornado nos
testes "adiantando" `tempo_ultimo_passo`, para que cada chamada a
`atualizar_movimento` processe exatamente um passo da sequência, de forma
determinística e sem depender de tempo real de execução.
"""

import pygame

from src.barreira import Barreira
from src.blocos import BlocoDireita, BlocoRepetir
from src.item import Item
from src.objetivo import Objetivo
from src.personagem import Personagem
from src.pontuacao import Pontuacao


def _forcar_proximo_passo(personagem):
    """Garante que o próximo `atualizar_movimento` execute um passo,
    ignorando o delay entre comandos."""
    personagem.tempo_ultimo_passo = pygame.time.get_ticks() - personagem.delay_entre_passos - 1


def _matriz_vazia(linhas=1, colunas=3):
    return [[None for _ in range(colunas)] for _ in range(linhas)]


def test_movimento_direita_em_celula_livre():
    matriz = _matriz_vazia()
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem

    personagem.iniciar_programacao([BlocoDireita(0, 0)])
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)

    assert (personagem.linha, personagem.coluna) == (0, 1)
    assert matriz[0][1] is personagem
    assert matriz[0][0] is None


def test_bloco_repetir_e_expandido_em_varios_passos():
    matriz = _matriz_vazia(1, 5)
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem

    repetir = BlocoRepetir(0, 0, n=3)
    repetir.comandos = [BlocoDireita(0, 0)]
    personagem.iniciar_programacao([repetir])

    assert len(personagem.comandos_expandidos) == 3

    for _ in range(3):
        _forcar_proximo_passo(personagem)
        personagem.atualizar_movimento(matriz)

    assert personagem.coluna == 3


def test_colisao_com_barreira_nao_move_personagem():
    matriz = _matriz_vazia(1, 3)
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem
    matriz[0][1] = Barreira(50, (255, 0, 0))

    personagem.iniciar_programacao([BlocoDireita(0, 0)])
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)

    assert (personagem.linha, personagem.coluna) == (0, 0)
    assert matriz[0][0] is personagem


def test_coletar_item_remove_item_do_mapa_e_soma_pontuacao():
    matriz = _matriz_vazia(1, 2)
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem
    matriz[0][1] = Item()
    pontuacao = Pontuacao()

    personagem.iniciar_programacao([BlocoDireita(0, 0)], pontuacao=pontuacao)
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)

    assert personagem.coluna == 1
    assert matriz[0][1] is personagem  # item foi coletado e substituído pelo personagem
    assert pontuacao.pontos == 10


def test_chegar_no_objetivo_marca_flag_e_nao_perde_vida():
    matriz = _matriz_vazia(1, 2)
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem
    matriz[0][1] = Objetivo()
    vidas_iniciais = personagem.vidas

    personagem.iniciar_programacao([BlocoDireita(0, 0)])
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)  # executa o movimento até o objetivo
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)  # processa o fim da sequência

    assert personagem.chegou_no_objetivo is True
    assert personagem.vidas == vidas_iniciais
    assert personagem.executando_comandos is False


def test_nao_chegar_ao_objetivo_perde_vida_e_volta_a_posicao_inicial():
    matriz = _matriz_vazia(1, 3)
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem
    vidas_iniciais = personagem.vidas

    personagem.iniciar_programacao([BlocoDireita(0, 0)])  # termina sem alcançar o objetivo
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)  # move para (0, 1)
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)  # processa o fim da sequência -> perde 1 vida

    assert personagem.vidas == vidas_iniciais - 1
    assert personagem.chegou_no_objetivo is False
    assert (personagem.linha, personagem.coluna) == (0, 0)
    assert matriz[0][0] is personagem


def test_movimento_para_fora_da_matriz_nao_quebra_e_nao_move():
    matriz = _matriz_vazia(1, 1)
    personagem = Personagem(0, 0)
    matriz[0][0] = personagem

    personagem.iniciar_programacao([BlocoDireita(0, 0)])  # não existe coluna 1
    _forcar_proximo_passo(personagem)
    personagem.atualizar_movimento(matriz)

    assert (personagem.linha, personagem.coluna) == (0, 0)
    assert matriz[0][0] is personagem
