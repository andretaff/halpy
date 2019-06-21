import time
import threading
import queue

q = queue.Queue()


def temporizador(miliSegundos):
    inicio = time.time()
    while (time.time()+0.001<inicio+miliSegundos):
        time.sleep(0.001)
        if not q.empty():
            comando = q.get(True,1)
            if comando == 'stop':
                break


def pararThread():
    q.put('stop')



def iniciarThread(tipoTempo,tempo):
    t = 0
    if tipoTempo == 0:
        t = threading.Thread(target = temporizador,args=(999999999,))
    if tipoTempo == 1:
       t = threading.Thread(target = temporizador,args=(tempo,))
    return t
