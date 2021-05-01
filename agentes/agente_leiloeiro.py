from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.acl.filters import Filter
from pade.behaviours.protocols import FipaSubscribeProtocol, TimedBehaviour

class PublisherProtocol(FipaSubscribeProtocol):

    def __init__(self, agent):
        super(PublisherProtocol, self).__init__(agent,
                                                   message=None,
                                                   is_initiator=False)

    def handle_subscribe(self, message):
        self.register(message.sender)
        display_message(self.agent.aid.name, message.content)
        resposta = message.create_reply()
        resposta.set_performative(ACLMessage.AGREE)
        resposta.set_content('OK')
        self.agent.send(resposta)

    def handle_cancel(self, message):
        self.deregister(self, message.sender)
        display_message(self.agent.aid.name, message.content)

    def notify(self, message):
        super(PublisherProtocol, self).notify(message)


class AgenteLeiloeiro(Agent):
    def __init__(self, aid, f):
        super(AgenteLeiloeiro, self).__init__(aid=aid, debug=False)
        self.f = f
        self.protocol = PublisherProtocol(self)
        self.behaviours.append(self.protocol)

    # def react(self, message):
    #     super(AgenteLeiloeiro, self).react(message)
    #     if self.f.filter(message):
    #         if f'{message.content}'.startswith("registro:"):
    #             display_message(self.aid.localname,
    #                             f'Registrando {message.sender.name}')

