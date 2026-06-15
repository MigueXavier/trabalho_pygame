class Pontuacao:
    def __init__(self):
        self.pontos = 0

    def adicionar_pontos(self):
        self.pontos += 10

    def resetar(self):
        self.pontos = 0