import engine.temporizador
import interface.fenString
import engine.transpTable
import engine.board
import engine.negamax
import threading
import time

class Game(threading.Thread):
    def __init__(self,tamanhoTT,output):
        threading.Thread.__init__(self)
        self.tabela = engine.transpTable.TranspTable(tamanhoTT)
        self.tabuleiro = engine.board.Tabuleiro()
        self.fenReader = interface.fenString.fenString()
        self.output = output
        self.negaMax = engine.negamax.Negamax(self.tabuleiro, self.tabela,self.output)
        self.listaComandos = []
        self.ativa = True


    def run(self):
        while self.ativa:
            if len(self.listaComandos)>0:
                comando = self.listaComandos.pop()
                if comando[0] == 0:
                    self.reiniciar()
                if comando[0] == 1:
                    self.realizarMovimento(comando[1])
                if comando[0]==2:
                    self.buscarMovimento(comando[1],comando[2])
                if comando[0] ==3:
                    self.parar()
                    
            time.sleep(0.01)



    def comandoReiniciar(self):
        self.listaComandos.append([0])
    
    def comandoRealizarMovimento(self, mov):
        self.listaComandos.append([1,mov])

    def comandoBuscarMovimento(self,tipotempo,tempo):
        self.listaComandos.append([2,tipotempo,tempo])

    def comandoParar(self):
        self.listaComandos.append([3])


    def parar(self):
        engine.temporizador.pararThread()

    def reiniciar(self):
        del self.tabuleiro
        del self.negaMax
        self.tabuleiro = self.fenReader.tabuleiroPadrao()
        self.negaMax = engine.negamax.Negamax(self.tabuleiro, self.tabela,self.output)

    def realizarMovimento(self,movimentoUser):
        movs = self.tabuleiro.genMovimentos()
        for movimento in movs:
            movimento.print()
            if movimento.compara(movimentoUser):
                self.tabuleiro.realizarMovimento(movimento)

        

    def buscarMovimento(self,tipoTempo, tempo):
        self.temporizador = engine.temporizador.iniciarThread(tipoTempo,tempo)
        self.temporizador.start()
        self.negaMax = engine.negamax.Negamax(self.tabuleiro, self.tabela,self.output)
        self.negaMax.iniciar(self.temporizador)
        self.negaMax.start()




