import engine.board
class Avaliador(object):
    def avaliar(board):
        if board.corMover == 0:
            return board.vBranco - board.vPreto
        else:
            return board.vPreto - board.vBranco


