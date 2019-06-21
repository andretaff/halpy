import engine.transpItem

class TranspTable(object):
    def __init__(self,maxRegistros):
        self.tabela = []
        self.maxReg = maxRegistros
        self.hits = 0
        for i in range(maxRegistros):
            item = engine.transpItem.TranspItem(0,0,0,0,0)
            self.tabela.append(item)

    def armazenar(self,transpItem):
        self.tabela[transpItem.chave%self.maxReg] = transpItem

    def recuperar(self,chave,profundidade,idade):
        item = self.tabela[chave%self.maxReg]
        if item == 0:
            return False,0
        hit = item.chave == chave and item.profundidade >=profundidade and item.idade == idade 
        if hit:
            self.hits = self.hits +1
        return hit,item