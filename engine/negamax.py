import engine.board
import engine.avaliador


class Negamax():
    """description of class"""
    def __init__(self,tabuleiro):
        self.avaliador = engine.avaliador.Avaliador()
        self.tabuleiro = tabuleiro

    def run(self, alfa, beta, profundidade):
        if profundidade == 0:
            return self.avaliador.avaliar(self.tabuleiro)
        else:
            valor = -9999999999
            listaMovs = self.tabuleiro.genMovimentos()
            for mov in listaMovs:
                #mov.print()
                self.tabuleiro.realizarMovimento(mov)
                #mov.print()
                #self.tabuleiro.print()
                if self.tabuleiro.invalido():
                    novoValor = +99999999
                else:
                    novoValor = -self.run(-beta,-alfa, profundidade - 1)
                self.tabuleiro.desfazerMovimento(mov)
                if novoValor > valor:
                    valor = novoValor
                    if (self.maxProf == profundidade):
                        self.melhorMov = mov
                if alfa<valor:
                    alfa = valor
                if alfa>beta:
                    break
            return valor

    def iniciar(self):
        self.maxProf = 5
        self.run(-9999999999,+9999999999,self.maxProf)
        self.melhorMov.print()



