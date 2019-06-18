# -*- coding: utf-8 -*-
from engine import negamax,board
import interface.fenString

fenReader = interface.fenString.fenString()

tabuleiro = fenReader.tabuleiroPadrao()

tabuleiro.print()

negamax = negamax.Negamax(tabuleiro)

mov = negamax.iniciar()

mov.print()