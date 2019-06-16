# -*- coding: utf-8 -*-
from engine import *
import interface.fenString

fenReader = interface.fenString.fenString()

tabuleiro = fenReader.tabuleiroPadrao()

tabuleiro.print()

lMovs = tabuleiro.genMovimentos()
for mov in lMovs:
    mov.print()
