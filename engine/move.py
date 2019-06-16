# -*- coding: utf-8 -*-
import engine.constants
import engine.bitboard

class Movimento:
    def __init__(self,lado,peca,pecaCaptura,tipo,bbDe,bbPara,roque,enpassant):
        self.lado = lado
        self.peca = peca
        self.pecaCaptura = pecaCaptura
        self.tipo = tipo
        self.bbDe = bbDe
        self.bbPara = bbPara
        self.roque = roque
        self.enpassant = enpassant
        
    def print(self):
        if self.tipo == engine.constants.MNORMAL:
            linha = 'M NORMAL'
        elif self.tipo == engine.constants.MDUPLO:
            linha = 'M DUPLO'
        elif self.tipo == engine.constants.MCAP:
            linha = 'CAPTURA '
        elif self.tipo == engine.constants.MROQUEPEQ:
            linha = 'ROQUE PEQUENO '
            if self.lado == 0:
                linha = linha + ' BRANCO '
            else:
                linha = linha + ' PRETO '
            print(linha)
            return
        elif self.tipo == engine.constants.MROQUEGRD:
            linha = 'ROQUE GRANDE '
            if self.lado == 0:
                linha = linha + ' BRANCO '
            else:
                linha = linha + ' PRETO '
            print(linha)
            return
        linha = linha + engine.constants.pecas[self.peca]
        if self.lado == 0:
            linha = linha + ' BRANCO DE '
        else:
            linha = linha + ' PRETO DE '
        linha = linha + engine.bitboard.bbHumano(self.bbDe)+ ' PARA '+engine.bitboard.bbHumano(self.bbPara)
        if self.tipo == engine.constants.MCAP:
            linha = linha + ' CAPT '+engine.constants.pecas[self.pecaCaptura]
        print (linha)