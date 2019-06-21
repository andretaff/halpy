import unittest
import engine.negamax
import engine.move
import interface.fenString
import engine.bitboard
import  time
import datetime

class Test_mateIn2(unittest.TestCase):
    def test_A(self):
        arquivo = open('.\\tests\\matein2.txt','r')
        linhas = arquivo.readlines()
        fen = ''
        fenReader = interface.fenString.fenString()
        nTeste = 0
        tabela = engine.transpTable.TranspTable(5999999)
        start_time = time.time()
        hTot = 0
        for linha in linhas:
            if len(linha)>10 and linha[0:10]== '##########':
                break
            if len(linha)<3 or linha[0]=='#' or (not fenReader.ehValido(linha) and fen == ''):
                if len(linha)>3:
                    print (linha)
                continue
            if fen == '':
                fen = linha
            else:
                linha = linha.replace('x','')
                peca = linha[0]
                casa =linha[1:3]
                bb = engine.bitboard.humanoBB(casa)
                tabuleiro = fenReader.lerFenString(fen)
                negamax = engine.negamax.Negamax(tabuleiro,tabela)
                negamax.movCount = nTeste
                #tabuleiro.print()
                mov = negamax.iniciar()
                #mov.print()
                self.assertEqual((engine.constants.pecas[mov.peca]).upper(),(peca).upper())
                self.assertEqual(mov.bbPara,bb)
                nTeste = nTeste +1
                print ("Teste "+str(nTeste)+ ' ok - '+str(tabela.hits)+' hits')
                hTot = hTot + tabela.hits
                tabela.hits = 0
                print (fen)
                mov.print()
                print ('------------------------------------------------')
                fen = ''
                del negamax
                del tabuleiro
                del mov

        elapsed_time = time.time() - start_time

        arquivo.close()
        arquivo = open('matein2results.txt','a')
        arquivo.write('-----------\n')
        arquivo.write('Versao '+ engine.constants.VERSAO+'\n') 
        arquivo.write(datetime.datetime.now().strftime('%d/%m/%Y %H:%M')+'\n')
        arquivo.write(str(nTeste) +' testes \n'+str(elapsed_time)+ ' time\n'+str(hTot)+' hits\n'+str(tabela.maxReg)+' posicoes\n')    
        arquivo.close()


if __name__ == '__main__':
    unittest.main()
