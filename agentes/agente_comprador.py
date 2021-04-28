from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent

class AgenteComprador(Agent):
    def __init__(self, aid, nome, dinheiro = 0):
        super(AgenteComprador, self).__init__(aid=aid)
        self.nome = nome
        self.dinheiro = dinheiro
        display_message(self.aid.localname, 'Hello World!')
    
    def lance(ultimo_lance):
        if(ultimo_lance > self.dinheiro * 0.6 ):
            display_message(self.aid.localname, 'Não possuo mais dinheiro')
            return ultimo_lance
        return ultimo_lance + 1
    
    def comprar(ultimo_lance):
        self.dinheiro -= ultimo_lance


        


