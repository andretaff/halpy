# -*- coding: utf-8 -*-

VITORIA = 99999999
DERROTA = -VITORIA
EMPATE = -100

PECA_NENHUM = 0xFF
PPW = 0
PKW = 2
PBW = 4
PRW = 6
PQW = 8
PGW = 10

PPB = 1
PKB = 3
PBB = 5
PRB = 7
PQB = 9
PGB = 11

WHITE = 0
BLACK = 1

PW = 12
PB = 13

ALLBITBOARDS = 16
POSITION_NONE = 0

ROQUE_NENHUM = 0
ROQUE_PW = 0x00000000000000FF
ROQUE_GW = 0x000000000000FF00
ROQUE_PB = 0x0000000000FF0000
ROQUE_GB = 0x00000000FF000000

R={}
R[1] = 0x00000000000000FF
R[2] = 0x000000000000FF00
R[3] = 0x0000000000FF0000
R[4] = 0x00000000FF000000
R[5] = 0x000000FF00000000
R[6] = 0x0000FF0000000000
R[7] = 0x00FF000000000000
R[8] = 0xFF00000000000000

C={}
C[1] = 0x0101010101010101
C[2] = 0x0202020202020202
C[3] = 0x0404040404040404
C[4] = 0x0808080808080808
C[5] = 0x1010101010101010
C[6] = 0x2020202020202020
C[7] = 0x4040404040404040
C[8] = 0x8080808080808080

index={}
mCavalo = {}
mRei = {}
aPeao = []
aPeao.append({})
aPeao.append({})
k = 0
for i in range(8):
    for j in range(8):
        index[k] = R[i+1]&C[j+1]
        
        #print (index[i*8+j])
        pos = index[k]
        mCavalo[k] = ((pos & (~R[8]) & (~(C[1]|C[2])))<<6)
        mCavalo[k] = (pos & (~ R[8]) & (~(C[1] | C[2]))) << 6
        mCavalo[k] = mCavalo[k] | (pos & (~ R[8]) & (~(C[7] | C[8])))<<10
        mCavalo[k] = mCavalo[k] | (pos & (~ (R[7] | R[8])) & (~C[8]))<<17
        mCavalo[k] = mCavalo[k] | (pos & (~ (R[7] | R[8])) & (~C[1]))<<15
        mCavalo[k] = mCavalo[k] | (pos & (~ (R[1] | R[2])) & (~C[8]))>>15
        mCavalo[k] = mCavalo[k] | (pos & (~ (R[1] | R[2])) & (~C[1]))>>17
        mCavalo[k] = mCavalo[k] | (pos & (~R[1]) & (~(C[1] | C[2])))>>10
        mCavalo[k] = mCavalo[k] | (pos & (~R[1]) & (~(C[7] | C[8])))>>6
        

        mRei[k] = (pos & (~R[8]))<<8
        mRei[k] = mRei[k] | (pos & (~R[1]))>>8
        mRei[k] = mRei[k] | (pos & (~C[1]))>>1
        mRei[k] = mRei[k] | (pos & (~C[8]))<<1
        mRei[k] = mRei[k] | (pos & (~(R[8]|C[1])))<<7
        mRei[k] = mRei[k] | (pos & (~(R[8]|C[8])))<<9
        mRei[k] = mRei[k] | (pos & (~(R[1]|C[1])))>>9
        mRei[k] = mRei[k] | (pos & (~(R[1]|C[8])))>>7

        aPeao[0][k] = (pos & (~C[1])) >> 9
        aPeao[0][k] = aPeao[0][k] | (pos & (~C[8])) >> 7
        aPeao[1][k] = (pos & (~C[1])) << 7
        aPeao[1][k] = aPeao[1][k] | (pos & (~C[8])) << 9
        
        k = k + 1


pecas = 'PpNnBbRrQqKk'

lsb_64_table= [63, 30,  3, 32, 59, 14, 11, 33,60, 24, 50,  9, 55, 19, 21, 34,61, 29,  2, 53, 51, 23, 41, 18,56, 28,  1, 43, 46, 27,  0, 35,  62, 31, 58,  4,  5, 49, 54,  6,  15, 52, 12, 40,  7, 42, 45, 16,   25, 57, 48, 13, 10, 39,  8, 44,   20, 47, 38, 22, 17, 37, 36, 26]

MNORMAL = 0
MDUPLO = 1
MCAP = 2
MROQUEPEQ = 3
MROQUEGRD = 4
MPROMO = 5
MPROMOCAP = 30

valores = [100,100,300,300,320,320,500,500,900,900,0,0]


VERSAO = 'ALPHA 0 MJ.003 (single threading)'