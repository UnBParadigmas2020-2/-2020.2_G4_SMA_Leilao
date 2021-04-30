from pade.misc.utility import display_message, call_later
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID

class AgenteComprador(Agent):
    def __init__(self, aid, f, dinheiro = 0):
        super(AgenteComprador, self).__init__(aid=aid)
        self.dinheiro = dinheiro
        self.f = f
        display_message(self.aid.localname, 'O agente {} possue R${}'.format(self.aid.localname, self.dinheiro))
    
    def lance(ultimo_lance):
        if(ultimo_lance > self.dinheiro * 0.6 ):
            display_message(self.aid.localname, 'Não possuo mais dinheiro')
            return ultimo_lance
        return ultimo_lance + 1
    
    def comprar(ultimo_lance):
        self.dinheiro -= ultimo_lance

    def on_start(self):
        super(AgenteComprador, self).on_start()
        display_message(self.aid.localname, 'Registrando-me no leilão...')
        call_later(8.0, self.sending_message)

    def sending_message(self):
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('leiloeiro'))
        message.set_content(f'registro:{self.aid.localname}')
        self.send(message)

    def react(self, message):
        super(AgenteComprador, self).react(message)
        if self.f.filter(message):
            display_message(self.aid.localname,
                            'Mensagem recebida from {}'.format(message.sender.name))

        


