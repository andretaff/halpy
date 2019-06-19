import engine.board
import engine.avaliador


class Negamax():
    """description of class"""
    def __init__(self,tabuleiro):
        self.avaliador = engine.avaliador.Avaliador()
        self.tabuleiro = tabuleiro
        self.print = False

    def run(self, alfa, beta, profundidade):
        movs = 0
        if profundidade == 0:
            return self.avaliador.avaliar(self.tabuleiro)
        else:
            valor = -9999999999
            tabValue = 0
            listaMovs = self.tabuleiro.genMovimentos()
            for mov in listaMovs:
#                if mov.tipo >= 3:
#                    self.tabuleiro.print()
#                if profundidade == self.maxProf:
#                    print('-------------------------------------------------------')
#                    self.tabuleiro.print()
#                    mov.print()
#                    #if mov.peca == 8 and mov.bbPara == engine.constants.index[22]:
##                    self.print = True
#                    print('-------------------------------------------------------') #19
                tabValue = self.tabuleiro.vBranco + self.tabuleiro.vPreto
                if self.print:
                    mov.print()
                self.tabuleiro.realizarMovimento(mov)
                if self.print:
                    self.tabuleiro.print()
                if not self.tabuleiro.invalido():
                    movs = movs + 1
                    novoValor = -self.run(-beta,-alfa, profundidade - 1)
                    if novoValor > valor:
                        valor = novoValor
                        if (self.maxProf == profundidade):
                            self.melhorMov = mov
                    if alfa<valor:
                        alfa = valor
                    if alfa>beta:
                        self.tabuleiro.desfazerMovimento(mov)
                        break
                self.tabuleiro.desfazerMovimento(mov)
                if self.tabuleiro.vBranco + self.tabuleiro.vPreto != tabValue:
                    print ('erro')
                    mov.print()

            if movs>0:
                return alfa
            else:
                if self.tabuleiro.emCheque():
                    return engine.constants.DERROTA#-(self.maxProf -profundidade)
                else:
                    return engine.constants.EMPATE

    def iniciar(self):
        self.maxProf = 4   
        self.run(-9999999999,+9999999999,self.maxProf)
        return self.melhorMov



