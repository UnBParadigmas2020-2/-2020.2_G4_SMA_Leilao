from pade.behaviours.protocols import FipaSubscribeProtocol, TimedBehaviour
from pade.misc.utility import display_message
from pade.acl.messages import ACLMessage, AID
from pade.core.agent import Agent

# Protocolo do editor. Com isso, compradores podem assinar esse protocolo
# e todas as vezes que o leiloeiro envia uma mensagem por esse protocolo
# todos os compradores recebem
class PublisherProtocol(FipaSubscribeProtocol):

    def __init__(self, agent):
        super(PublisherProtocol, self).__init__(agent,
                                                   message=None,
                                                   is_initiator=False)

    # É executado quando um comprador solicita inclusao no protocolo, no caso
    # isso seria registro no leilao
    def handle_subscribe(self, message):
        self.register(message.sender)
        self.agent.logger.log(self.agent.aid.name, message.content)
        resposta = message.create_reply()
        resposta.set_performative(ACLMessage.AGREE)
        resposta.set_content('OK')
        self.agent.send(resposta)

    def handle_cancel(self, message):
        self.deregister(self, message.sender)
        self.agent.logger.log(self.agent.aid.name, message.content)

    # Manda as mensagens
    def notify(self, message):
        super(PublisherProtocol, self).notify(message)


# Comportamento que executa de tempos em tempos e analisa os lances recebidos
# É aqui que vemos o atual melhor lance e provavelmente aqui definiremos um ganhador
# em algum momento
class AnalisaLances(TimedBehaviour):

    def __init__(self, agent, notify):
        super(AnalisaLances, self).__init__(agent, 10)
        self.notify = notify
        self.agent = agent

    def on_time(self):
        super(AnalisaLances, self).on_time()
        message = ACLMessage(ACLMessage.INFORM)
        message.set_protocol(ACLMessage.FIPA_SUBSCRIBE_PROTOCOL)

        # Se ja tiverem lances registrados, vemos o atual maior lance e definimos ele como novo minimo
        if self.agent.lances:
            # Verifica se existe apenas um agente concorrente
            # Caso positivo o vencedor é declarado e o programa é encerrado.
            print(list(self.agent.lances.keys()))
            print(list(self.agent.lances.values()))
            novo_lance_minimo =  max(self.agent.lances.values())
            if len(self.agent.lances) == 1:
                winner = list(self.agent.lances.keys())[0]
                self.agent.logger.log(self.agent.aid.name, f'O vencedor foi o comprador {winner}!')
                message = ACLMessage(ACLMessage.INFORM)
                message.set_protocol(ACLMessage.FIPA_REQUEST_PROTOCOL)
                message.add_receiver(AID(winner))
                message.set_content(f'vencedor: {winner}')
            else:
                self.agent.logger.log(self.agent.aid.name, f'Novo valor a bater {novo_lance_minimo}')

        # Caso contrario, damos o primeiro lance minimo do leilao. Que deveria vir do objeto leiloado    
        else:
            novo_lance_minimo = self.agent.objeto_leiloado.valor_inicial
            self.agent.logger.log(self.agent.aid.name, 'Iniciando leilão do item {} com valor inicial de R${}'.format(self.agent.objeto_leiloado.nome, novo_lance_minimo))

        # usa o protocolo do editor para mandar o novo lance minimo a todos os compradores
        self.agent.lances.clear()
        message.set_content(f'lance:{novo_lance_minimo}')
        self.notify(message)

class AgenteLeiloeiro(Agent):

    # dicionario para guardar os lances do leilao, as chaves sao os compradores
    # e os valores sao os lances em si
    lances = {}

    # inicializando agente, protocolos e comportamentos
    def __init__(self, aid, f, objeto, logger):
        super(AgenteLeiloeiro, self).__init__(aid=aid, debug=False)
        self.f = f
        self.logger = logger
        self.objeto_leiloado = objeto
        self.protocol = PublisherProtocol(self)
        self.behaviours.append(self.protocol)
        self.analisa_lances = AnalisaLances(self, self.protocol.notify)
        self.behaviours.append(self.analisa_lances)
    
    def on_start(self):
        super(AgenteLeiloeiro, self).on_start()

    # isso aqui executa toda vez que algum comprador manda uma mensagem ao leiloeiro
    def react(self, message):
        super(AgenteLeiloeiro, self).react(message)

        if self.f.filter(message):

            # o prefixo lance esta sendo usado para identificar que é um lance do comprador
            if f'{message.content}'.startswith("lance:"):
                lance = float(message.content.split(":")[1])

                #registramos o lance no nosso dicionario, que será analisado pelo AnalisaLances
                self.lances[message.sender.name] = lance
                
                self.logger.log(self.aid.localname,
                                f'Lance recebido de {message.sender.name}, {lance} reais')

