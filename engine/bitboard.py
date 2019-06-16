import engine.constants

def bbHumano(bb):
    i = indice(bb)
    
    linhas ='12345678'
    colunas = 'abcdefgh'

    return colunas[int(i%8)] + linhas[(7-int(i/8))]

def indice(bitboard):
    bitboard = bitboard ^ (bitboard-1)
    bitboard = (bitboard& 0xffffffff) ^ (bitboard >> 32)
    index = ((bitboard * 0x78291ACF)& 0xffffffff) >> 26
    return engine.constants.lsb_64_table[index]
