
from pathlib import Path
from util import rand64


caminho = Path('./chaves.txt')
chaves = []
if caminho.is_file():
    pass
else:
    rnd = rand64.Rand64()
    for pecas in range(14):
        chaves.append([])
        for posicoes in range(64):
            chaves[pecas].append(rnd.next())
    chaveBTM = rnd.next()
    chaveR = []
    for i in range(4):
        chaveR.append(rnd.next())
    arquivo = open('chaves.txt','w')
    for coluna in chaves:
        for item in coluna:
            arquivo.write(str(item)+' ')
       
    arquivo.write(str(chaveBTM)+' ')
    for chave in chaveR:
        arquivo.write(str(chave)+' ')
    arquivo.close()
chaves = []
chaveR = []
arquivo = open('chaves.txt','r')
linhas = arquivo.readlines()
for linha in linhas:
    linha = linha + ' '
    inteiros = [int(x) for x in linha.split()]
    posInt = 0
    for i in range(14):
        chaves.append([])
        for j in range(64):
            chaves[i].append(inteiros[posInt])
            posInt = posInt + 1
    chaveBTm = inteiros[posInt]
    posInt = posInt + 1
    for i in range (4):
        chaveR.append(inteiros[posInt])
        posInt = posInt + 1
arquivo.close()


del arquivo
del posInt
del i
del j
del linhas
