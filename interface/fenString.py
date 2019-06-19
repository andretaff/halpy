# -*- coding: utf-8 -*-
import engine.constants
import engine.board

class fenString:
    def lerFenString(self,fenString):
        tipo = 0
        self.tabuleiro = engine.board.Tabuleiro()
        posicao = 0
        for i in fenString:
            if i==' ':
                tipo = tipo + 1 
                continue
            if tipo == 0:
                if i=='/':
                    continue
                if i.isdigit():
                    posicao = posicao + int(i)
                else:
                    iPeca = 0
                    for peca in engine.constants.pecas:
                        if peca == i:
                            self.tabuleiro.adicionarPecaHumana(iPeca, posicao)
                        iPeca = iPeca + 1
                    posicao = posicao + 1
            if tipo == 1:
                if i=='w':
                    self.tabuleiro.corMover = 0
                else:
                    self.tabuleiro.corMover = 1
            if tipo == 2:
                if i == '-':
                    continue
                if i =='q':
                    self.tabuleiro.roque = self.tabuleiro.roque | engine.constants.ROQUE_GB
                if i == 'Q':
                    self.tabuleiro.roque = self.tabuleiro.roque | engine.constants.ROQUE_GW
                if i =='k':
                    self.tabuleiro.roque = self.tabuleiro.roque | engine.constants.ROQUE_PB
                if i == 'K':
                    self.tabuleiro.roque = self.tabuleiro.roque | engine.constants.ROQUE_PW
        return self.tabuleiro
    
    def tabuleiroPadrao(self):
        #return self.lerFenString('r4br1/3b1kpp/1q1P4/1pp1RP1N/p7/6Q1/PPB3PP/2KR4 w - - 1 0')
        return self.lerFenString('r4br1/3b1kp1/1q1P2p1/1pp1RP1N/p7/8/PPB3PP/2KR4 w - - 0 2')
        #return self.lerFenString('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq')

