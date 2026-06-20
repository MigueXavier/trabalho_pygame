

VIDAS_INICIAIS = 3


class Vidas:
    def __init__(self):
        self.quantidade = VIDAS_INICIAIS

    def perder(self):
        if self.quantidade > 0:
            self.quantidade -= 1
        return self.quantidade > 0

    def acabou(self):
        return self.quantidade <= 0

    def resetar(self):
        self.quantidade = VIDAS_INICIAIS
