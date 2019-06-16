import board
import avaliador


class negamax(object):
    """description of class"""
    def __init__(self,tabuleiro):
        self.avaliador = avaliador.Avaliador()
        self.tabuleiro = tabuleiro


    def run(self, alfa, beta, profundidade):
        if profundidade == 0:
            return avaliador.avaliar(tabuleiro)
        else:
            valor = -9999999999
            listaMovs = self.tabuleiro.genMovimentos()
            for mov in listaMovs:
                self.tabuleiro.realizarMovimento(mov)
                novoValor = -self.run(profundidade - 1,-beta,-alfa)
                if novoValor > valor:
                    valor = novoValor
                if alfa<novoValor:
                    alfa = novoValor
                if alfa>beta:
                    break
            return valor

    def iniciar(self):
        self.run(-9999999999,+9999999999,5)



