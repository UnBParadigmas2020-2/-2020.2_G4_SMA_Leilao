from agentes.agente_comprador import AgenteComprador
from agentes.agente_leiloeiro import AgenteLeiloeiro
from pade.misc.utility import start_loop
from pade.acl.aid import AID
from sys import argv
from random import *
from pade.acl.messages import ACLMessage
from pade.acl.filters import Filter


def main():
  f = Filter()
  f.performative = ACLMessage.INFORM
  agents = list()
  port = int(argv[1]) 
  agent_dinheiro = randint(100,1000)
  agente_leiloeiro = AgenteLeiloeiro(
      AID(name=f'leiloeiro@localhost:{port}'),f)
  agents.append(agente_leiloeiro)  
  port += 1
  numero_de_compradores=3
  for i in range(numero_de_compradores):
      agente_comprador = AgenteComprador(AID(name=f'comprador_{i}@localhost:{port+i}'), f, agent_dinheiro)
      agents.append(agente_comprador)
  start_loop(agents)

if __name__ == '__main__':
  main()