# -*- coding: utf-8 -*-

import interface.uci
import time
import threading

uci = interface.uci.UCI()

def inputThread():
    while uci.ativa:
        comando = input()
        uci.addComandoIn(comando)
        time.sleep(0.3)



uci.start()
inp = threading.Thread(target = inputThread,args=())
inp.start()

while uci.ativa:
    time.sleep(0.1)

