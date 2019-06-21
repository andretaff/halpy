import threading
import interface.game
import queue

class UCI(threading.Thread):
    """description of class"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.ativa = True
        self.game = interface.game.Game(5999999,self)
        self.game.start()
        self.filaIn = queue.Queue()
        self.filaOut = queue.Queue()
        
    def run(self):
        while self.ativa:
            if not self.filaIn.empty():
                comando = self.filaIn.get()
                if 'id' == comando:
                    self.filaOut.put(self.id())
                if 'isready' == comando:
                    self.comandosOut.append(self.isready())
                if 'position' in comando:
                    self.position(comando)
                if 'quit' == comando:
                    self.ativa = False
                    self.game.ativa = False
                    break
                if comando[0:2]=='go':
                    self.go(comando[2:])
                if 'stop' == comando:
                    self.game.comandoParar()

            if not (self.filaOut.empty()):
                comando = self.filaOut.get()
                print (comando)

    def addComandoIn(self,comando):
        self.filaIn.put(comando)

    def addComandoOut(self,comando):
        self.filaOut.put(comando)



    def id(self):
        return 'id name HalChess\nid author André Taffarello\nuciok\n'

 
    def position(self,params):
        paramList = params.split()
        if 'startpos' in paramList:
            self.game.reiniciar()
        if paramList[1]=='fen':
            for j in range(2,30):
                if j>len(paramList):
                    self.addComandoOut('Could not find moves')
                    return #ERRO FEIO
                if paramList[j]=='moves':
                    break
                strFen = strFen + ' '+paramList[j]
            self.game.prepararPosicao(strFen)


        for k in range(len(paramList)):
            if paramList[k]=='moves':
                break
        k = k +1
        while k<len(paramList):
            movimento = paramList[k]
            if not self.game.realizarMovimento(movimento):
                self.addComandoOut('Invalid moves')
            k = k + 1



    def isready(self):
        return 'readyok\n'

    def go(self,params):
        lParams = params.split()
        gMoveTime = False
        gTipo = 0
        tempo = 0


        for param in lParams:
            if param == 'movetime':
                gMoveTime = True
                gTipo = 1
            elif gMoveTime:
                tempo = int(param)

        mov = self.game.comandoBuscarMovimento(gTipo,tempo)


