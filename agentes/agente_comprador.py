from pade.behaviours.protocols import FipaSubscribeProtocol
from pade.misc.utility import display_message, call_later
from pade.acl.messages import ACLMessage
from pade.core.agent import Agent
from pade.acl.aid import AID
from random import randint


# Protocolo do assinante. Assina o protocolo do leiloeiro
# e com isso toda vez que o leiloeiro mandar uma mensagem nesse protocolo
# todos os compradores recebem
class SubscriberProtocol(FipaSubscribeProtocol):

    def __init__(self, agent, message):
        super(SubscriberProtocol, self).__init__(agent,
                                                 message,
                                                 is_initiator=True)

    # leiloeiro confirmou o registro do comprador
    def handle_agree(self, message):
        self.agent.logger.log(self.agent.aid.name, "Confirmação recebida")
    
    # isso executa toda vez que o comprador recebe uma mensagem atraves desse protocolo
    def handle_inform(self, message):
        self.agent.lance(message.content)

class AgenteComprador(Agent):

    # inicializando comprador
    def __init__(self, aid, f, logger, dinheiro = 0):
        super(AgenteComprador, self).__init__(aid=aid)
        self.logger = logger
        self.dinheiro = dinheiro
        self.f = f
        self.logger.log(self.aid.localname, 'O agente {} possue R${}'.format(self.aid.localname, self.dinheiro))

    # helper function para mandar uma mensagem ao leiloeiro, usada pra enviar o lance do comprador
    def send_message(self, msg):
        message = ACLMessage(ACLMessage.INFORM)
        message.add_receiver(AID('leiloeiro'))
        message.set_content(msg)
        self.send(message)

    # faz a assinatura no protocolo do leiloeiro, para receber mensagens referentes ao novo lance minimo 
    def launch_subscriber_protocol(self):
        message = ACLMessage(ACLMessage.SUBSCRIBE)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)
        message.set_content(f'Registro: {self.aid.localname}')
        message.add_receiver(AID('leiloeiro'))
        self.protocol = SubscriberProtocol(self, message)
        self.behaviours.append(self.protocol)
        self.protocol.on_start()

   # rola quando  o agente é iniciado
    def on_start(self):
        super(AgenteComprador, self).on_start()

        # chama a funcao que faz a assinatura do protocolo do leiloeiro
        # isso apos 8 segundos, pra dar tempo do leiloeiro ter iniciado
        self.logger.log(self.aid.localname, 'Registrando-me no leilão...')
        call_later(8.0, self.launch_subscriber_protocol)

    # essa funcao é executada pelo SubscriberProtocol, quando recebemos o novo lance minimo do leiloeiro
    # É aqui que fazemos o nosso lance e enviamos ao leiloeiro
    def lance(self, msg):
        if str(msg).startswith("lance"):
            lance_minimo = float(str(msg).split(":")[1])
            
            # um criterio arbitrario, dizendo que o comprador nao vai dar um lance maior que 60% da grana que ele tem
            if(lance_minimo >= self.dinheiro):
                print('sem grana')
                # retirar agente do leilão
            else:
                # manda mensagem ao leiloeiro com o lance
                valor_desejado = lance_minimo + lance_minimo * 0.4
                valor =  self.dinheiro if valor_desejado > self.dinheiro else valor_desejado
                novo_lance = randint(lance_minimo, int(valor))
                self.send_message(f"lance:{novo_lance}")

        
    # Essa funcao aqui serve pra reagir a uma mensagem recebida pelo leiloeiro
    def react(self, message):
        super(AgenteComprador, self).react(message)
        if self.f.filter(message):

            # A ideia aqui é que o leiloeiro mandaria pro comprador uma mensagem com o prefixo vencedor
            # quando ele vencesse o leilao. Nesse caso o leiloeiro manda uma mensagem pra um comprador especifico
            # por isso nao usamos o SubscriberProtocol, que é pra quando a mensagem é pra todos os compradores 
            if f'{message.content}'.startswith("vencedor:"):
                # Aqui provavelmente encerrariamos as atividades
                self.agent.log(self.aid.localname,
                                f'Venci o leilao')