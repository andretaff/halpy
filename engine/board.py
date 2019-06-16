# -*- coding: utf-8 -*-
import engine.constants, engine.move
import engine.bitboard

class Tabuleiro:
    def __init__(self):
        self.corMover = engine.constants.WHITE
        self.board = []
        self.vBranco = 0
        self.vPreto = 0
        self.roque = engine.constants.ROQUE_NENHUM
        for i in range(engine.constants.ALLBITBOARDS):
            self.board.append(engine.constants.POSITION_NONE)
     
    def indice(self,bitboard):
        bitboard = bitboard ^ (bitboard-1)
        bitboard = (bitboard& 0xffffffff) ^ (bitboard >> 32)
        index = ((bitboard * 0x78291ACF)& 0xffffffff) >> 26
        return engine.constants.lsb_64_table[index]

    def getPecaBB(cor,bb):
        i = cor
        peca = engine.constants.PECA_NENHUM
        while i <= engine.constants.GB:
            if self.board[i]&bb:
                return i
            i = i + 2
        return peca


    def adicionarPecaHumana(self,peca, posicao):
        self.adicionarPeca(peca,2**posicao)
        
    def adicionarPeca(self,peca,bitboard):
        self.board[peca] ^= bitboard
        if peca%2==0:
            self.board[engine.constants.PW] ^= bitboard
            self.vBranco = self.vBranco + engine.constants.valores[peca]
        else:
            self.board[engine.constants.PB] ^= bitboard
            self.vPreto = self.vPreto + engine.constants.valores[peca]


    def removerPeca(self,peca,bitboard):
        self.board[peca] ^= bitboard
        if peca%2==0:
            self.board[engine.constants.PW] ^= bitboard
            self.vBranco = self.vBranco - engine.constants.valores[peca]
        else:
            self.board[engine.constants.PB] ^= bitboard
            self.vPreto = self.vPreto - engine.constants.valores[peca]

    def realizarMovimento(self,movimento):
        if movimento.tipo == engine.constants.MNORMAL:
            self.removerPeca(movimento.peca,movimento.bbDe)
            self.adicionarPeca(movimento.peca,movimento.bbPara)
        if movimento.tipo == engine.constants.MDUPLO:
            self.removerPeca(movimento.peca,movimento.bbDe)
            self.adicionarPeca(movimento.peca,movimento.bbPara)
            if self.corMover == 0:
                self.enPassant = movimento.bbPara >> 8
            else:
                self.enPassant = movimento.bbPara << 8

        if movimento.tipo == engine.constants.MCAP:
            self.removerPeca(movimento.peca,movimento.bbDe)
            self.removerPeca(movimento.pecaCaptura, movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbPara)

        self.corMover = 1-self.corMover

    def desfazerMovimento(self,movimento):
        if movimento.tipo == engine.constants.MNORMAL:
            self.removerPeca(movimento.peca,movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)
        if movimento.tipo == engine.constants.MDUPLO:
            self.removerPeca(movimento.peca,movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)

        if movimento.tipo == engine.constants.MCAP:
            self.removerPeca(movimento.peca,movimento.bbPara)
            self.adicionarPeca(movimento.pecaCaptura,movimento.bbDePara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)

        self.corMover = 1-self.corMover
    def print(self):
        linha = ''
        for i in range(64):
            bitboard = (2**i) 
            achou = False
            for j in range(engine.constants.PGB+1):
                if (bitboard & self.board[j])!=0:
                    linha = linha + engine.constants.pecas[j]
                    achou = True
                    break
            if not achou:
                linha = linha + ' '
            if ((i+2) % 8 == 1):
                print (linha)
                linha = ''
        print (linha)               
    
    def genMovsCavalo(self, lista):
        if self.corMover == 0:
            peca = engine.constants.PKW
            bb = self.board[peca]
            bbAmigos = self.board[engine.constants.PW]
            bbInimigos = self.board[engine.constants.PB]
            bbTodas = bbAmigos | bbInimigos
        else:
            peca = engine.constants.PKB
            bb = self.board[peca]
            bbAmigos = self.board[engine.constants.PB]
            bbInimigos = self.board[engine.constants.PW]
            bbTodas = bbAmigos | bbInimigos
        while bb>0:
            pos = (bb & -bb) & 0xffffffffffffffff
            index = self.indice(pos)
            bbTo = engine.constants.mCavalo[index] & ~bbTodas
            while bbTo>0:
                lsb = (bbTo & -bbTo)  & 0xffffffffffffffff
                mov = engine.move.Movimento(self.corMover,
                                            peca,
                                            0,
                                            engine.constants.MNORMAL,
                                            pos,
                                            lsb)
                lista.append(mov)
                bbTo = bbTo & (bbTo -1)
            bb = bb & (bb-1)

    def genMovsTorre(self,peca,lista):
        bbb = 0
        if self.corMover == 0:
            bbb = self.board[peca]
        else:
            bbb = self.board[peca]

        bbTodas = self.board[engine.constants.PW] | self.board[engine.constants.PB]

        while bbb>0:
            bb = (bbb & -bbb)  & 0xffffffffffffffff 
            if (bb != 0) and (bb & (engine.constants.R[1]) == 0):
                bbTo = bb >> 8
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & engine.constants.R[1]) != 0:
                        break
                    bbTo = bbTo >> 8
            if (bb != 0) and (bb & (engine.constants.R[8]) == 0):
                bbTo = bb << 8
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & engine.constants.R[8]) != 0:
                        break
                    bbTo = bbTo << 8

            if (bb != 0) and (bb & (engine.constants.C[1]) == 0):
                bbTo = bb >> 1
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & engine.constants.C[1]) != 0:
                        break
                    bbTo = bbTo >> 1

            if (bb != 0) and (bb & (engine.constants.C[8]) == 0):
                bbTo = bb << 1
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & engine.constants.C[8]) != 0:
                        break
                    bbTo = bbTo << 1
            bbb = (bbb & (bbb-1))


    def genMovsBispo(self,peca,lista):
        bbb = 0
        if self.corMover == 0:
            bbb = self.board[peca]
        else:
            bbb = self.board[peca]

        bbTodas = self.board[engine.constants.PW] | self.board[engine.constants.PB]

        while bbb>0:
            bb = (bbb & -bbb)  & 0xffffffffffffffff 
            if (bb != 0) and (bb & (engine.constants.R[1]|engine.constants.C[1]) == 0):
                bbTo = bb >> 9
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    mov.print()
                    if (bbTo & (engine.constants.R[1]|engine.constants.C[1])) != 0:
                        break
                    bbTo = bbTo >> 9

            if (bb != 0) and (bb & (engine.constants.R[1]|engine.constants.C[8]) == 0):
                bbTo = bb >> 7
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & (engine.constants.R[1]|engine.constants.C[8]) != 0):
                        break
                    bbTo = bbTo >> 7


            if (bb != 0) and (bb & (engine.constants.R[8]|engine.constants.C[1]) == 0):
                bbTo = bb << 7
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & (engine.constants.R[8]|engine.constants.C[1]) != 0):
                        break
                    bbTo = bbTo << 7

            if (bb != 0) and (bb & (engine.constants.R[8]|engine.constants.C[8]) == 0):
                bbTo = bb << 9
                while (bbTo&bbTodas==0):
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                bb,
                                                bbTo)
                    lista.append(mov)
                    if (bbTo & (engine.constants.R[8]|engine.constants.C[8]) != 0):
                        break
                    bbTo = bbYo << 9
            bbb = (bbb & (bbb-1))

    def genMovsPeao(self,lista):
        if self.corMover == engine.constants.WHITE:
            peca = engine.constants.PPW
            bb = self.board[peca]
            bbAmigos = self.board[engine.constants.PW]
            bbInimigos = self.board[engine.constants.PB]
            bbTodas = bbAmigos | bbInimigos
            normais = (bb>>8) & ~ bbTodas
            duplos = ((normais & engine.constants.R[6]) >> 8) & ~bbTodas

            while duplos > 0:
                lsb = (duplos & -duplos)  & 0xffffffffffffffff
                mov = engine.move.Movimento(engine.constants.WHITE,
                                            peca,
                                            0,
                                            engine.constants.MDUPLO,
                                            lsb<<16,
                                            lsb)
                lista.append(mov)
                duplos = duplos & (duplos -1)

            while normais > 0:
                lsb = (normais & -normais) & 0xffffffffffffffff
                mov = engine.move.Movimento(engine.constants.WHITE,
                                            peca,
                                            0,
                                            engine.constants.MNORMAL,
                                            lsb<<8,
                                            lsb)
                lista.append(mov)
                normais = normais & (normais -1)
        else:
            peca = engine.constants.PPB
            bb = self.board[peca]
            bbAmigos = self.board[engine.constants.PB]
            bbInimigos = self.board[engine.constants.PW]
            bbTodas = bbAmigos | bbInimigos
            normais = (bb<<8) & ~ bbTodas
            duplos = ((normais & engine.constants.R[3]) << 8) & ~bbTodas

            while duplos > 0:
                lsb = (duplos & -duplos)  & 0xffffffffffffffff
                mov = engine.move.Movimento(self.corMover,
                                            peca,
                                            0,
                                            engine.constants.MDUPLO,
                                            lsb>>16,
                                            lsb)
                lista.append(mov)
                duplos = duplos & (duplos -1)

            while normais > 0:
                lsb = (normais & -normais) & 0xffffffffffffffff
                mov = engine.move.Movimento(self.corMover,
                                            peca,
                                            0,
                                            engine.constants.MNORMAL,
                                            lsb>>8,
                                            lsb)
                lista.append(mov)
                normais = normais & (normais -1)

    def genMovsRei(self,lista,capturas):
        peca = self.corMover + engine.constants.PGW
        bb = self.board[peca]
        bbTodas = self.board[engine.constants.PB] | self.board[engine.constants.PW]
        if capturas:
            bbInimigas = self.board[engine.constants.PB-self.corMover] 
            bbTo = engine.constants.mRei[self.indice(bb)]&bbInimigas
        else:
            bbTo = engine.constants.mRei[self.indice(bb)]&~bbTodas
        while bbTo > 0:
            lsb = (bbTo & -bbTo) & 0xffffffffffffffff
            if capturas:
                pecaAlvo = self.getPecaBB(1-self.corMover,lsb)
                tipo = engine.constants.MCAP
            else:
                pecaAlvo = 0xFF
                tipo = engine.constants.MNORMAL
            mov = engine.move.Movimento(self.corMover,
                                        peca,
                                        pecaAlvo,
                                        tipo,
                                        bb,
                                        lsb)
            lista.append(mov)
            bbTo = bbTo & (bbTo -1)

            
    def genMovimentos(self):
        self.listaMovs = []
        self.genMovsPeao(self.listaMovs)
        self.genMovsCavalo(self.listaMovs)
        self.genMovsBispo(engine.constants.PBW+self.corMover, self.listaMovs)
        self.genMovsTorre(engine.constants.PRW+self.corMover, self.listaMovs)
        self.genMovsBispo(engine.constants.PQW+self.corMover, self.listaMovs)
        self.genMovsTorre(engine.constants.PQW+self.corMover, self.listaMovs)
        self.genMovsRei(self.listaMovs,False)
        return self.listaMovs

