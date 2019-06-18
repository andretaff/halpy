import engine.constants

def bbHumano(bb):
    i = indice(bb)
    
    linhas ='12345678'
    colunas = 'abcdefgh'

    return colunas[int(i%8)] + linhas[(7-int(i/8))]

def humanoBB(casa):
    soma = 0
    for letra in 'abcdefgh':
        if letra == casa[0]:
            break
        soma = soma + 1
    i = 0
    for linha in range(8):
        if casa[1] == str(linha+1):
            soma = soma + (8*(7-i))
            break
        i = i + 1
    return engine.constants.index[soma]


def indice(bitboard):
    bitboard = bitboard ^ (bitboard-1)
    bitboard = (bitboard& 0xffffffff) ^ (bitboard >> 32)
    index = ((bitboard * 0x78291ACF)& 0xffffffff) >> 26
    return engine.constants.lsb_64_table[index]
