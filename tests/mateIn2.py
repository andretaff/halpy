import unittest
import engine.negamax
import engine.move
import interface.fenString
import engine.bitboard

class Test_mateIn2(unittest.TestCase):
    def test_A(self):
        arquivo = open('.\\tests\\matein2.txt','r')
        linhas = arquivo.readlines()
        fen = ''
        fenReader = interface.fenString.fenString()
        nTeste = 0
        for linha in linhas:
            if len(linha)==0 or linha[0]=='#':
                continue
            if fen == '':
                fen = linha
            else:
                mov = linha
                peca = linha[0]
                casa =linha[1:3]
                bb = engine.bitboard.humanoBB(casa)
                tabuleiro = fenReader.lerFenString(fen)
                negamax = engine.negamax.Negamax(tabuleiro)
                #tabuleiro.print()
                mov = negamax.iniciar()
                #mov.print()
                self.assertEqual(engine.constants.pecas[mov.peca],peca)
                self.assertEqual(mov.bbPara,bb)
                fen = ''
                nTeste = nTeste +1
                print ("Teste "+str(nTeste)+ ' ok ')
                del negamax
                del tabuleiro
                del mov

        arquivo.close()

            


if __name__ == '__main__':
    unittest.main()