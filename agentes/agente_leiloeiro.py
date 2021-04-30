from pade.misc.utility import display_message
from pade.core.agent import Agent
from pade.acl.messages import ACLMessage
from pade.acl.aid import AID
from pade.acl.filters import Filter


class AgenteLeiloeiro(Agent):
    def __init__(self, aid, f):
        super(AgenteLeiloeiro, self).__init__(aid=aid, debug=False)
        self.f = f

    def react(self, message):
        super(AgenteLeiloeiro, self).react(message)
        if self.f.filter(message):
            if f'{message.content}'.startswith("registro:"):
                display_message(self.aid.localname,
                                f'Registrando {message.sender.name}')

