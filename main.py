from agentes.agente_comprador import AgenteComprador
from agentes.agente_leiloeiro import AgenteLeiloeiro
from classes.objeto_leiloado import ObjetoLeiloado
from classes.logger import Logger
from pade.misc.utility import start_loop
from pade.acl.messages import ACLMessage
from pade.acl.filters import Filter
from pade.acl.aid import AID
from random import randint
from sys import argv

def main():

  # para troca de mensagens esparsas entre leiloeiro e compradores
  f = Filter()
  f.performative = ACLMessage.INFORM

  agents = list()
  port = int(argv[1]) 

  logger = Logger()

  # criando objeto a ser leiloado
  objeto = ObjetoLeiloado('Vaso Antigo', 40)
  
  # criando agente leiloeiro
  agente_leiloeiro = AgenteLeiloeiro(
      AID(name=f'leiloeiro@localhost:{port}'),f, objeto, logger)
  agents.append(agente_leiloeiro)  

  port += 1
  numero_de_compradores=3
  
  for i in range(numero_de_compradores):
      # criando agentes compradores
      agent_dinheiro = randint(100,1000)
      agente_comprador = AgenteComprador(AID(name=f'comprador_{i}@localhost:{port+i}'), f, logger,agent_dinheiro)
      agents.append(agente_comprador)

  start_loop(agents)

if __name__ == '__main__':
  main()