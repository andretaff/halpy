# -*- coding: utf-8 -*-
import engine.constants
import engine.bitboard

class Movimento:
    def __init__(self,lado,peca,pecaCaptura,tipo,bbDe,bbPara,roque,enpassant,indiceDe,indicePara):
        self.lado = lado
        self.peca = peca
        self.pecaCaptura = pecaCaptura
        self.tipo = tipo
        self.bbDe = bbDe
        self.bbPara = bbPara
        self.roque = roque
        self.enpassant = enpassant
        self.indiceDe = indiceDe
        self.indicePara = indicePara

        
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
        elif self.tipo> engine.constants.MPROMOCAP:
            linha = ' PROMOÇÃO PARA '+engine.constants.pecas[self.tipo- engine.constants.MPROMOCAP]+ ' CAPTURANDO '
        elif self.tipo> engine.constants.MPROMO:
            linha = ' PROMOÇÃO PARA '+engine.constants.pecas[self.tipo- engine.constants.MPROMO]+ ' '


        linha = linha + engine.constants.pecas[self.peca]
        if self.lado == 0:
            linha = linha + ' BRANCO DE '
        else:
            linha = linha + ' PRETO DE '
        linha = linha + engine.bitboard.bbHumano(self.bbDe)+ ' PARA '+engine.bitboard.bbHumano(self.bbPara)
        if (self.tipo== engine.constants.MCAP) or (self.tipo> engine.constants.MPROMOCAP):
            linha = linha + ' CAPT '+engine.constants.pecas[self.pecaCaptura]
        print (linha)

    def compara(self,strMov):
        casa1 = strMov[0:2]
        casa2 = strMov[2:4]
        pecaPromo = ''
        if len(strMov)>4:
            pecaPromo = strMov[4]

        if casa1 == 'e1' and casa2 == 'g1':
            return  self.lado == 0 and self.tipo == MROQUEPEQ
        if casa1 == 'e1' and casa2 == 'b1':
            return self.lado == 0 and self.tipo == MROQUEGRD
        if casa1 == 'e8' and casa2 == 'g8':
            return  self.lado == 1 and self.tipo == MROQUEPEQ
        if casa1 == 'e8' and casa2 == 'b8':
            return self.lado == 1 and self.tipo == MROQUEGRD

        bbFrom = engine.bitboard.bbHumano(self.bbDe)
        bbTo   = engine.bitboard.bbHumano(self.bbPara)
        result = True
        pecaPromoMov = -1
        if self.tipo> engine.constants.MPROMOCAP:
            pecaPromoMov = self.tipo - engine.constants.MPROMOCAP
        elif self.tipo> engine.constants.MPROMO:
            pecaPromoMov = self.tipo - engine.constants.MPROMO
        if pecaPromo != '':
            result = engine.constants.pecas[pecaPromoMov].upper() == pecaPromo.upper()
        result = result and (bbFrom == casa1)
        result = result and (bbTo == casa2)
        return result

    def str(self):
        if self.tipo==engine.constants.MROQUEPEQ and self.lado == 0:
            return 'e1g1'

        if self.tipo==engine.constants.MROQUEGRD and self.lado == 0:
            return 'e1b1'

        if self.tipo==engine.constants.MROQUEPEQ and self.lado == 1:
            return 'e8g8'

        if self.tipo==engine.constants.MROQUEGRD and self.lado == 1:
            return 'e8b8'
        
        saida=engine.bitboard.bbHumano(self.bbDe) + engine.bitboard.bbHumano(self.bbPara)

        pecaPromoMov = ''
        if self.tipo> engine.constants.MPROMOCAP:
            pecaPromoMov = self.tipo - engine.constants.MPROMOCAP
        elif self.tipo> engine.constants.MPROMO:
            pecaPromoMov = self.tipo - engine.constants.MPROMO
        if pecaPromoMov != '':
            saida = saida + engine.constants.pecas[pecaPromoMov].lower()

        return saida


        


