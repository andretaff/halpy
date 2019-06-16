# -*- coding: utf-8 -*-
import engine.constants
import engine.bitboard

class Movimento:
    def __init__(self,lado,peca,pecaCaptura,tipo,bbDe,bbPara):
        self.lado = lado
        self.peca = peca
        self.pecaCaptura = pecaCaptura
        self.tipo = tipo
        self.bbDe = bbDe
        self.bbPara = bbPara
    
    def print(self):
        if self.tipo == engine.constants.MNORMAL:
            linha = 'M NORMAL'
        elif self.tipo == engine.constants.MDUPLO:
            linha = 'M DUPLO'
        linha = linha + engine.constants.pecas[self.peca]
        if self.lado == 0:
            linha = linha + ' BRANCO DE '
        else:
            linha = linha + ' PRETO DE '
        linha = linha + engine.bitboard.bbHumano(self.bbDe)+ ' PARA '+engine.bitboard.bbHumano(self.bbPara)
        print (linha)