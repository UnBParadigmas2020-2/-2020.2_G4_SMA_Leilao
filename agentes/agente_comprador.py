# agent_example_1.py
# A simple hello agent in PADE!

from pade.misc.utility import display_message, start_loop
from pade.core.agent import Agent

class AgenteComprador(Agent):
    def __init__(self, aid, nome, dinheiro = 0):
        super(AgenteComprador, self).__init__(aid=aid)
        self.nome = nome
        self.dinheiro = dinheiro
        display_message(self.aid.localname, 'Hello World!')


