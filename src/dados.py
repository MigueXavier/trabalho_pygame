import json
import os

ARQUIVO_SAVE = "dados.json"

dados_padrao = {
    "highscore": 0,
    "fase_atual": 1
}

class Data:
    @staticmethod
    def carregar_dados():
        if os.path.exists(ARQUIVO_SAVE):
            with open(ARQUIVO_SAVE, "r") as arquivo:
                try:
                    return json.load(arquivo)
                except json.JSONDecodeError:
                    return dados_padrao
        return dados_padrao

    @staticmethod
    def salvar_dados(dados):
        with open(ARQUIVO_SAVE, "w") as arquivo:
            json.dump(dados, arquivo, indent=4)

    @staticmethod
    def existe_save():
        return os.path.exists(ARQUIVO_SAVE) and os.path.getsize(ARQUIVO_SAVE) > 0
