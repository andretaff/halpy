# -*- coding: utf-8 -*-
import engine.constants
import engine.board

class fenString:
    def lerFenString(self,fenString):
        self.tabuleiro = engine.board.Tabuleiro()
        posicao = 0
        for i in fenString:
            if i==' ':
                break
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
        return self.tabuleiro
    
    def tabuleiroPadrao(self):
        #return self.lerFenString('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        return self.lerFenString('rnbqkbnr/pppppppp/8/8/8/8/8/RNBQKBNR')

