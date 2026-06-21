"""Testes para src.dados.Data (persistência de progresso/recorde)."""

import json

from src import dados as modulo_dados
from src.dados import Data, dados_padrao


def test_carregar_dados_retorna_padrao_quando_arquivo_nao_existe(tmp_path, monkeypatch):
    caminho = tmp_path / "dados.json"
    monkeypatch.setattr(modulo_dados, "ARQUIVO_SAVE", str(caminho))

    resultado = Data.carregar_dados()

    assert resultado == dados_padrao


def test_salvar_e_carregar_dados_round_trip(tmp_path, monkeypatch):
    caminho = tmp_path / "dados.json"
    monkeypatch.setattr(modulo_dados, "ARQUIVO_SAVE", str(caminho))

    dados_para_salvar = {"highscore": 50, "fase_atual": 3}
    Data.salvar_dados(dados_para_salvar)

    assert caminho.exists()
    assert Data.carregar_dados() == dados_para_salvar


def test_carregar_dados_com_arquivo_corrompido_retorna_padrao(tmp_path, monkeypatch):
    caminho = tmp_path / "dados.json"
    caminho.write_text("{ isso nao é json valido ", encoding="utf-8")
    monkeypatch.setattr(modulo_dados, "ARQUIVO_SAVE", str(caminho))

    resultado = Data.carregar_dados()

    assert resultado == dados_padrao


def test_existe_save_false_quando_nao_ha_arquivo(tmp_path, monkeypatch):
    caminho = tmp_path / "dados.json"
    monkeypatch.setattr(modulo_dados, "ARQUIVO_SAVE", str(caminho))

    assert Data.existe_save() is False


def test_existe_save_false_quando_arquivo_vazio(tmp_path, monkeypatch):
    caminho = tmp_path / "dados.json"
    caminho.write_text("", encoding="utf-8")
    monkeypatch.setattr(modulo_dados, "ARQUIVO_SAVE", str(caminho))

    assert Data.existe_save() is False


def test_existe_save_true_apos_salvar(tmp_path, monkeypatch):
    caminho = tmp_path / "dados.json"
    monkeypatch.setattr(modulo_dados, "ARQUIVO_SAVE", str(caminho))

    Data.salvar_dados(dados_padrao)

    assert Data.existe_save() is True
    # também garante que o conteúdo gravado é um JSON válido
    with open(caminho, "r") as arquivo:
        assert json.load(arquivo) == dados_padrao
