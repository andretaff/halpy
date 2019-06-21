import engine.board
import engine.avaliador
import engine.transpTable
import engine.transpItem
import threading



class Negamax(threading.Thread):
    """description of class"""
    def __init__(self,tabuleiro,transp,output):
        threading.Thread.__init__(self)
        self.avaliador = engine.avaliador.Avaliador()
        self.tabuleiro = tabuleiro
        self.print = False
        self.transp = transp
        self.tHits = 0
        self.melhorNov = 0
        self.movCount = 0
        self.output = output

    def run(self):
        self.maxProf = 10   
        self.tHits = 0
        self.curProf = 1
        self.realMov = 0
        self.nodes = 0
        while (self.temporizador.isAlive()):
            nota = self.nega(-9999999999,+9999999999,self.curProf)
            if self.temporizador.isAlive():
                self.realMov = self.melhorMov
                if self.realMov!=0:
                    self.output.addComandoOut('info depth '+str(self.curProf)+' cp '+str(nota)+ ' tbhits '+str(self.tHits)+ ' nodes '+str(self.nodes)+ ' pv '+self.realMov.str())
            self.curProf = self.curProf +1
        self.output.addComandoOut('bestmove '+ self.realMov.str())



    def nega(self, alfa, beta, profundidade):
        movs = 0
        chave = self.tabuleiro.chave
        tOk, tItem = self.transp.recuperar(chave,profundidade,self.movCount)
        melhorMov = 0
        self.nodes = self.nodes +1
        if tOk:
            self.tHits = self.tHits + 1 
            if profundidade == self.curProf:
                self.melhorMov = tItem.movimento
            return tItem.score

        if profundidade == 0:
            return self.avaliador.avaliar(self.tabuleiro)
        else:
            valor = -9999999999
            tabValue = 0
            listaMovs = self.tabuleiro.genMovimentos()
            for mov in listaMovs:
                if not self.temporizador.isAlive():
                    return 0
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
#                if self.print:
#                    mov.print()
                self.tabuleiro.realizarMovimento(mov)
#                if self.print:
#                    self.tabuleiro.print()
                if not self.tabuleiro.invalido():
                    movs = movs + 1
                    novoValor = -self.nega(-beta,-alfa, profundidade - 1)
                    if novoValor > valor:
                        valor = novoValor
                        melhorMov = mov
                        if profundidade == self.curProf:
                            self.melhorMov = melhorMov

                    if alfa<valor:
                        alfa = valor
                    if alfa>beta:
                        self.tabuleiro.desfazerMovimento(mov)
                        break
                self.tabuleiro.desfazerMovimento(mov)
                if self.tabuleiro.chave != chave:
                    print ('erro')
                    mov.print()

            if movs>0:
                tItem =engine.transpItem.TranspItem(chave,alfa,profundidade,self.movCount,melhorMov)
                self.transp.armazenar(tItem)
                return alfa
            else:
                if self.tabuleiro.emCheque():
                    tItem =engine.transpItem.TranspItem(chave,engine.constants.DERROTA-(self.curProf -profundidade),profundidade,0,melhorMov)
                    self.transp.armazenar(tItem)
                    return engine.constants.DERROTA-(self.maxProf -profundidade)
                else:
                    tItem =engine.transpItem.TranspItem(chave,engine.constants.EMPATE-(self.curProf -profundidade),profundidade,0,melhorMov)
                    self.transp.armazenar(tItem)
                    return engine.constants.EMPATE

    def iniciar(self,temporizador):
        self.temporizador = temporizador

        self.maxProf = 10   
        self.tHits = 0
        self.curProf = 1
        self.realMov = 0
        self.melhorMov = 0




