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
        self.enPasant = 0
        self.check = False
        for i in range(engine.constants.ALLBITBOARDS):
            self.board.append(engine.constants.POSITION_NONE)

    def invalido(self):
        return self.casaAtacada(self.board[engine.constants.PGB-self.corMover],1-self.corMover)
     
    def indice(self,bitboard):
        bitboard = bitboard ^ (bitboard-1)
        bitboard = (bitboard& 0xffffffff) ^ (bitboard >> 32)
        index = ((bitboard * 0x78291ACF)& 0xffffffff) >> 26
        return engine.constants.lsb_64_table[index]

    def getPecaBB(self,cor,bb):
        i = cor
        peca = engine.constants.PECA_NENHUM
        while i <= engine.constants.PGB:
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

        if movimento.tipo == engine.constants.MROQUEPEQ:
            if self.corMover == 0:
                self.removerPeca(engine.constants.PGW,engine.constants.index[60])
                self.removerPeca(engine.constants.PRW,engine.constants.index[63])
                self.adicionarPeca(engine.constants.PGW,engine.constants.index[63])
                self.adicionarPeca(engine.constants.PRW,engine.constants.index[62])
            else:
                self.removerPeca(engine.constants.PGB,engine.constants.index[4])
                self.removerPeca(engine.constants.PRB,engine.constants.index[7])
                self.adicionarPeca(engine.constants.PGB,engine.constants.index[7])
                self.adicionarPeca(engine.constants.PRB,engine.constants.index[6])

        if movimento.tipo == engine.constants.MROQUEGRD:
            if self.corMover == 0:
                self.removerPeca(engine.constants.PGW,engine.constants.index[60])
                self.removerPeca(engine.constants.PRW,engine.constants.index[56])
                self.adicionarPeca(engine.constants.PGW,engine.constants.index[56])
                self.adicionarPeca(engine.constants.PRW,engine.constants.index[57])
            else:
                self.removerPeca(engine.constants.PGB,engine.constants.index[4])
                self.removerPeca(engine.constants.PRB,engine.constants.index[0])
                self.adicionarPeca(engine.constants.PGB,engine.constants.index[0])
                self.adicionarPeca(engine.constants.PRB,engine.constants.index[1])

        if movimento.tipo > engine.constants.MPROMOCAP:
            pecaPromo = movimento.tipo - engine.constants.MPROMOCAP
            self.removerPeca(movimento.peca,movimento.bbDe)
            self.removerPeca(movimento.pecaCaptura, movimento.bbPara)
            self.adicionarPeca(pecaPromo,movimento.bbPara)
        elif movimento.tipo> engine.constants.MPROMO:
            pecaPromo = movimento.tipo - engine.constants.MPROMO
            self.removerPeca(movimento.peca,movimento.bbDe)
            self.adicionarPeca(pecaPromo,movimento.bbPara)


                          




        self.corMover = 1-self.corMover
        movimento.roque = self.roque
        movimento.enPasant = self.enPasant



    def desfazerMovimento(self,movimento):
        if movimento.tipo == engine.constants.MNORMAL:
            self.removerPeca(movimento.peca,movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)
        if movimento.tipo == engine.constants.MDUPLO:
            self.removerPeca(movimento.peca,movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)

        if movimento.tipo == engine.constants.MCAP:
            self.removerPeca(movimento.peca,movimento.bbPara)
            self.adicionarPeca(movimento.pecaCaptura,movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)

        if movimento.tipo == engine.constants.MROQUEPEQ:
            if self.corMover == 1:
                self.removerPeca(engine.constants.PGW,engine.constants.index[63])
                self.removerPeca(engine.constants.PRW,engine.constants.index[62])
                self.adicionarPeca(engine.constants.PGW,engine.constants.index[60])
                self.adicionarPeca(engine.constants.PRW,engine.constants.index[63])
            else:
                self.removerPeca(engine.constants.PGB,engine.constants.index[7])
                self.removerPeca(engine.constants.PRB,engine.constants.index[6])
                self.adicionarPeca(engine.constants.PGB,engine.constants.index[4])
                self.adicionarPeca(engine.constants.PRB,engine.constants.index[7])

        if movimento.tipo == engine.constants.MROQUEGRD:
            if self.corMover == 1:
                self.removerPeca(engine.constants.PGW,engine.constants.index[56])
                self.removerPeca(engine.constants.PRW,engine.constants.index[57])
                self.adicionarPeca(engine.constants.PGW,engine.constants.index[60])
                self.adicionarPeca(engine.constants.PRW,engine.constants.index[56])
            else:
                self.removerPeca(engine.constants.PGB,engine.constants.index[0])
                self.removerPeca(engine.constants.PRB,engine.constants.index[1])
                self.adicionarPeca(engine.constants.PGB,engine.constants.index[4])
                self.adicionarPeca(engine.constants.PRB,engine.constants.index[0])

        if movimento.tipo > engine.constants.MPROMOCAP:
            pecaPromo = movimento.tipo - engine.constants.MPROMOCAP
            self.removerPeca(pecaPromo,movimento.bbPara)
            self.adicionarPeca(movimento.peca,movimento.bbDe)
            self.adicionarPeca(movimento.pecaCaptura, movimento.bbPara)

        elif movimento.tipo> engine.constants.MPROMO:
            pecaPromo = movimento.tipo - engine.constants.MPROMO
            self.adicionarPeca(movimento.peca,movimento.bbDe)
            self.removerPeca(pecaPromo,movimento.bbPara)


        self.corMover = 1-self.corMover
        self.enPasant = movimento.enPasant
        self.roque = movimento.roque


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
    
    def emCheque(self):
        return self.casaAtacada(self.board[engine.constants.PGW+self.corMover],self.corMover)

    def casaAtacada(self,bb,cor):
        casa = self.indice(bb)
        if engine.constants.aPeao[cor][casa] & self.board[engine.constants.PPB-cor] != 0:
            return True
        if engine.constants.mCavalo[casa] & self.board[engine.constants.PKB-cor] != 0:
            return True
        if engine.constants.mRei[casa] & self.board[engine.constants.PGB-cor] != 0:
            return True

        bbAmigas = self.board[engine.constants.PW+cor]
        bbInimigas =self.board[engine.constants.PB-cor]
        if (bb & (engine.constants.R[1] | engine.constants.C[1])==0):
            bbTo = bb >> 9
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.R[1] | engine.constants.C[1])!=0:
                    break
                bbTo = bbTo >> 9
            if (bbTo & (self.board[engine.constants.PBB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        if (bb & (engine.constants.R[1] | engine.constants.C[8])==0):
            bbTo = bb >> 7
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.R[1] | engine.constants.C[8])!=0:
                    break
                bbTo = bbTo >> 7
            if (bbTo & (self.board[engine.constants.PBB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        if (bb & (engine.constants.R[8] | engine.constants.C[1])==0):
            bbTo = bb << 7
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.R[8] | engine.constants.C[1])!=0:
                    break
                bbTo = bbTo << 7
            if (bbTo & (self.board[engine.constants.PBB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        if (bb & (engine.constants.R[8] | engine.constants.C[8])==0):
            bbTo = bb << 9
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.R[8] | engine.constants.C[8])!=0:
                    break
                bbTo = bbTo << 9
            if (bbTo & (self.board[engine.constants.PBB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        if (bb & (engine.constants.R[1])==0):
            bbTo = bb >> 8
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.R[1])!=0:
                    break
                bbTo = bbTo >> 8
            if (bbTo & (self.board[engine.constants.PRB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        if (bb & (engine.constants.R[8])==0):
            bbTo = bb << 8
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.R[8])!=0:
                    break
                bbTo = bbTo << 8
            if (bbTo & (self.board[engine.constants.PRB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True            

        if (bb & (engine.constants.C[1])==0):
            bbTo = bb >> 1
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.C[1])!=0:
                    break
                bbTo = bbTo >> 1
            if (bbTo & (self.board[engine.constants.PRB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        if (bb & (engine.constants.C[8])==0):
            bbTo = bb << 1
            while (not bbTo&bbAmigas!=0) and (not bbTo & bbInimigas !=0):
                if bbTo & (engine.constants.C[8])!=0:
                    break
                bbTo = bbTo <<1
            if (bbTo & (self.board[engine.constants.PRB-cor] | self.board[engine.constants.PQB-cor] ))!=0:
                return True

        return False

    def genMovsCavalo(self, lista,capturas):
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
            if not capturas:
                bbTo = engine.constants.mCavalo[index] & ~bbTodas
                while bbTo>0:
                    lsb = (bbTo & -bbTo)  & 0xffffffffffffffff
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                pos,
                                                lsb,
                                                self.roque,
                                                self.enPasant)
                    lista.append(mov)
                    bbTo = bbTo & (bbTo -1)
            else:
                bbTo = engine.constants.mCavalo[index] & bbInimigos
                while bbTo>0:
                    lsb = (bbTo & -bbTo)  & 0xffffffffffffffff
                    pecaTo = self.getPecaBB(1-self.corMover,lsb)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaTo,
                                                engine.constants.MCAP,
                                                pos,
                                                lsb,
                                                self.roque,
                                                self.enPasant)
                    lista.append(mov)
                    bbTo = bbTo & (bbTo -1)

            bb = bb & (bb-1)

    def genMovsTorre(self,peca,lista,capturas):
        bbb = 0
        if self.corMover == 0:
            bbb = self.board[peca]
        else:
            bbb = self.board[peca]

        bbTodas = self.board[engine.constants.PW] | self.board[engine.constants.PB]
        bbInimigas = self.board[engine.constants.PB-self.corMover]

        while bbb>0:
            bb = (bbb & -bbb)  & 0xffffffffffffffff 
            if (bb != 0) and (bb & (engine.constants.R[1]) == 0):
                bbTo = bb >> 8
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & engine.constants.R[1]) != 0:
                        break
                    bbTo = bbTo >> 8
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)
            if (bb != 0) and (bb & (engine.constants.R[8]) == 0):
                bbTo = bb << 8
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & engine.constants.R[8]) != 0:
                        break
                    bbTo = bbTo << 8
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)

            if (bb != 0) and (bb & (engine.constants.C[1]) == 0):
                bbTo = bb >> 1
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & engine.constants.C[1]) != 0:
                        break
                    bbTo = bbTo >> 1
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)

            if (bb != 0) and (bb & (engine.constants.C[8]) == 0):
                bbTo = bb << 1
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & engine.constants.C[8]) != 0:
                        break
                    bbTo = bbTo << 1
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)


            bbb = (bbb & (bbb-1))


    def genMovsBispo(self,peca,lista,capturas):
        bbb = 0
        if self.corMover == 0:
            bbb = self.board[peca]
        else:
            bbb = self.board[peca]

        bbTodas = self.board[engine.constants.PW] | self.board[engine.constants.PB]
        bbInimigas = self.board[engine.constants.PB-self.corMover]

        while bbb>0:
            bb = (bbb & -bbb)  & 0xffffffffffffffff 
            if (bb != 0) and (bb & (engine.constants.R[1]|engine.constants.C[1]) == 0):
                bbTo = bb >> 9
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)                                                
                        lista.append(mov)
                   
                    if (bbTo & (engine.constants.R[1]|engine.constants.C[1])) != 0:
                        break
                    bbTo = bbTo >> 9
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)


            if (bb != 0) and (bb & (engine.constants.R[1]|engine.constants.C[8]) == 0):
                bbTo = bb >> 7
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & (engine.constants.R[1]|engine.constants.C[8]) != 0):
                        break
                    bbTo = bbTo >> 7
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)

            if (bb != 0) and (bb & (engine.constants.R[8]|engine.constants.C[1]) == 0):
                bbTo = bb << 7
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & (engine.constants.R[8]|engine.constants.C[1]) != 0):
                        break
                    bbTo = bbTo << 7
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)

            if (bb != 0) and (bb & (engine.constants.R[8]|engine.constants.C[8]) == 0):
                bbTo = bb << 9
                while (bbTo&bbTodas==0):
                    if not capturas:
                        mov = engine.move.Movimento(self.corMover,
                                                    peca,
                                                    0,
                                                    engine.constants.MNORMAL,
                                                    bb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    if (bbTo & (engine.constants.R[8]|engine.constants.C[8]) != 0):
                        break
                    bbTo = bbTo << 9
                if capturas and (bbTo &bbInimigas):
                    pecaInimiga = self.getPecaBB(1-self.corMover,bbTo)
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                pecaInimiga,
                                                engine.constants.MCAP,
                                                bb,
                                                bbTo,
                                                self.roque,
                                                self.enPasant)                                                
                    lista.append(mov)
            bbb = (bbb & (bbb-1))

    def genMovsPeao(self,lista,capturas):
        if self.corMover == engine.constants.WHITE:
            peca = engine.constants.PPW
            bb = self.board[peca]
            bbAmigos = self.board[engine.constants.PW]
            bbInimigos = self.board[engine.constants.PB]
            bbTodas = bbAmigos | bbInimigos

            if not capturas:
                normais = (bb>>8) & ~ bbTodas
                promos = normais & engine.constants.R[1]
                normais = normais & ~promos
                duplos = ((normais & engine.constants.R[6]) >> 8) & ~bbTodas

                while promos>0:
                    lsb = (promos & -promos)  & 0xffffffffffffffff
                    for pecapromo in [engine.constants.PQW, engine.constants.PKW, engine.constants.PRW, engine.constants.PBW]:
                        mov = engine.move.Movimento(engine.constants.WHITE,
                                                    peca,
                                                    0,
                                                    engine.constants.MPROMO+pecapromo,
                                                    lsb<<8,
                                                    lsb,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    promos = promos & (promos -1)

                while duplos > 0:
                    lsb = (duplos & -duplos)  & 0xffffffffffffffff
                    mov = engine.move.Movimento(engine.constants.WHITE,
                                                peca,
                                                0,
                                                engine.constants.MDUPLO,
                                                lsb<<16,
                                                lsb,
                                                self.roque,
                                                self.enPasant)
                    lista.append(mov)
                    duplos = duplos & (duplos -1)

                while normais > 0:
                    lsb = (normais & -normais) & 0xffffffffffffffff
                    mov = engine.move.Movimento(engine.constants.WHITE,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                lsb<<8,
                                                lsb,
                                                self.roque,
                                                self.enPasant)
                    lista.append(mov)
                    normais = normais & (normais -1)
            else:
                lsb = bb
                while bb != 0:
                    lsb =(bb & -bb) & 0xffffffffffffffff
                    casa = self.indice(lsb)
                    bbToTodos = engine.constants.aPeao[0][casa] & bbInimigos
                    bbPromos = bbToTodos & engine.constants.R[1]
                    bbToTodos = bbToTodos & ~bbPromos

                    while bbPromos!=0:
                        bbTo = (bbPromos & -bbPromos) & 0xffffffffffffffff
                        pecaCap = self.getPecaBB(1,bbTo)
                        for pecapromo in [engine.constants.PQW, engine.constants.PKW, engine.constants.PRW, engine.constants.PBW]:
                            mov = engine.move.Movimento(engine.constants.WHITE,
                                                        peca,
                                                        pecaCap,
                                                        engine.constants.MPROMOCAP+pecapromo,
                                                        lsb,
                                                        bbTo,
                                                        self.roque,
                                                        self.enPasant)
                            lista.append(mov)
                        bbPromos = bbPromos &(bbPromos-1)

                    while bbToTodos != 0:
                        bbTo = (bbToTodos & -bbToTodos) & 0xffffffffffffffff
                        pecaCap = self.getPecaBB(1,bbTo)
                        mov = engine.move.Movimento(engine.constants.WHITE,
                                                    peca,
                                                    pecaCap,
                                                    engine.constants.MCAP,
                                                    lsb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                        bbToTodos = bbToTodos & (bbToTodos -1)
                    bb = bb & (bb-1)
        else:
            peca = engine.constants.PPB
            bb = self.board[peca]
            bbAmigos = self.board[engine.constants.PB]
            bbInimigos = self.board[engine.constants.PW]
            bbTodas = bbAmigos | bbInimigos
            if not capturas:
                normais = (bb<<8) & ~ bbTodas

                promos = normais & engine.constants.R[8]
                normais = normais & ~promos
                duplos = ((normais & engine.constants.R[3]) << 8) & ~bbTodas

                while promos>0:
                    lsb = (promos & -promos)  & 0xffffffffffffffff
                    for pecapromo in [engine.constants.PQB, engine.constants.PKB, engine.constants.PRB, engine.constants.PBB]:
                        mov = engine.move.Movimento(engine.constants.BLACK,
                                                    peca,
                                                    0,
                                                    engine.constants.MPROMO+pecapromo,
                                                    lsb>>8,
                                                    lsb,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                    promos = promos & (promos -1)



                while duplos > 0:
                    lsb = (duplos & -duplos)  & 0xffffffffffffffff
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MDUPLO,
                                                lsb>>16,
                                                lsb,
                                                self.roque,
                                                self.enPasant)
                    lista.append(mov)
                    duplos = duplos & (duplos -1)

                while normais > 0:
                    lsb = (normais & -normais) & 0xffffffffffffffff
                    mov = engine.move.Movimento(self.corMover,
                                                peca,
                                                0,
                                                engine.constants.MNORMAL,
                                                lsb>>8,
                                                lsb,
                                                self.roque,
                                                self.enPasant)
                    lista.append(mov)
                    normais = normais & (normais -1)
            else:
                lsb = bb
                while bb != 0:
                    lsb =(bb & -bb) & 0xffffffffffffffff
                    casa = self.indice(lsb)
                    bbToTodos = engine.constants.aPeao[1][casa] & bbInimigos

                    bbPromos = bbToTodos & engine.constants.R[8]
                    bbToTodos = bbToTodos & ~bbPromos

                    while bbPromos!=0:
                        bbTo = (bbPromos & -bbPromos) & 0xffffffffffffffff
                        pecaCap = self.getPecaBB(1,bbTo)
                        for pecapromo in [engine.constants.PQB, engine.constants.PKB, engine.constants.PRB, engine.constants.PBB]:
                            mov = engine.move.Movimento(engine.constants.BLACK,
                                                        peca,
                                                        pecaCap,
                                                        engine.constants.MPROMOCAP+pecapromo,
                                                        lsb,
                                                        bbTo,
                                                        self.roque,
                                                        self.enPasant)
                        bbPromos = bbPromos &(bbPromos-1)

                    while bbToTodos != 0:
                        bbTo = (bbToTodos & -bbToTodos) & 0xffffffffffffffff
                        pecaCap = self.getPecaBB(0,bbTo)
                        mov = engine.move.Movimento(engine.constants.BLACK,
                                                    peca,
                                                    pecaCap,
                                                    engine.constants.MCAP,
                                                    lsb,
                                                    bbTo,
                                                    self.roque,
                                                    self.enPasant)
                        lista.append(mov)
                        bbToTodos = bbToTodos & (bbToTodos -1)
                    bb = bb & (bb-1)

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
                                        lsb,
                                        self.roque,
                                        self.enPasant)
            lista.append(mov)
            bbTo = bbTo & (bbTo -1)

        if (not capturas):
            if self.corMover == 0:
                if self.roque & (engine.constants.ROQUE_PW) != 0:
                    if (bbTodas & (engine.constants.index[61]|engine.constants.index[62]))==0:
                        if (not  self.casaAtacada(engine.constants.index[61],0)) and (not  self.casaAtacada(engine.constants.index[62],0)) and (not  self.casaAtacada(engine.constants.index[60],0)) and (not  self.casaAtacada(engine.constants.index[63],0)):
                            mov = engine.move.Movimento(self.corMover,
                                                        peca,
                                                        0xFF,
                                                        engine.constants.MROQUEPEQ,
                                                        0,
                                                        0,
                                                        self.roque,
                                                        self.enPasant)
                            lista.append(mov)
                if self.roque & (engine.constants.ROQUE_GW) != 0:
                    if (bbTodas & (engine.constants.index[59]|engine.constants.index[58]|engine.constants.index[57]))==0:
                        if (not  self.casaAtacada(engine.constants.index[59],0)) and (not  self.casaAtacada(engine.constants.index[58],0)) and (not  self.casaAtacada(engine.constants.index[57],0)) and (not  self.casaAtacada(engine.constants.index[56],0)) and (not  self.casaAtacada(engine.constants.index[60],0)):
                            mov = engine.move.Movimento(self.corMover,
                                                        peca,
                                                        0xFF,
                                                        engine.constants.MROQUEGRD,
                                                        0,
                                                        0,
                                                        self.roque,
                                                        self.enPasant)
                            lista.append(mov)
            else:
                if self.roque & (engine.constants.ROQUE_PB) != 0:
                    if (bbTodas & (engine.constants.index[5]|engine.constants.index[6]))==0:
                        if (not  self.casaAtacada(engine.constants.index[5],1)) and (not  self.casaAtacada(engine.constants.index[6],1)) and (not  self.casaAtacada(engine.constants.index[7],0)) and (not  self.casaAtacada(engine.constants.index[4],0)):
                            mov = engine.move.Movimento(self.corMover,
                                                        peca,
                                                        0xFF,
                                                        engine.constants.MROQUEPEQ,
                                                        0,
                                                        0,
                                                        self.roque,
                                                        self.enPasant)
                            lista.append(mov)
                if self.roque & (engine.constants.ROQUE_GB) != 0:
                    if (bbTodas & (engine.constants.index[1]|engine.constants.index[2]|engine.constants.index[3]))==0:
                        if (not  self.casaAtacada(engine.constants.index[1],1)) and (not  self.casaAtacada(engine.constants.index[2],1)) and (not  self.casaAtacada(engine.constants.index[3],1)) and (not  self.casaAtacada(engine.constants.index[4],0)) and (not  self.casaAtacada(engine.constants.index[0],0)):
                            mov = engine.move.Movimento(self.corMover,
                                                        peca,
                                                        0xFF,
                                                        engine.constants.MROQUEGRD,
                                                        0,
                                                        0,
                                                        self.roque,
                                                        self.enPasant)
                            lista.append(mov)            
    def genMovimentos(self):
        self.listaMovs = []
        self.genMovsPeao(self.listaMovs,True)
        self.genMovsCavalo(self.listaMovs,True)
        self.genMovsBispo(engine.constants.PBW+self.corMover, self.listaMovs,True)
        self.genMovsTorre(engine.constants.PRW+self.corMover, self.listaMovs, True)
        self.genMovsBispo(engine.constants.PQW+self.corMover, self.listaMovs,True)
        self.genMovsTorre(engine.constants.PQW+self.corMover, self.listaMovs,True)
        self.genMovsRei(self.listaMovs,True)

        self.genMovsPeao(self.listaMovs,False)
        self.genMovsCavalo(self.listaMovs,False)
        self.genMovsBispo(engine.constants.PBW+self.corMover, self.listaMovs,False)
        self.genMovsTorre(engine.constants.PRW+self.corMover, self.listaMovs, False)
        self.genMovsBispo(engine.constants.PQW+self.corMover, self.listaMovs,False)
        self.genMovsTorre(engine.constants.PQW+self.corMover, self.listaMovs, False)
        self.genMovsRei(self.listaMovs,False)
        return self.listaMovs