from agentes.agente_comprador import AgenteComprador
from pade.misc.utility import start_loop
from pade.acl.aid import AID
from sys import argv
from random import *



def main():
  agents_per_process = 3
  c = 0
  agents = list()
  for i in range(agents_per_process):
      port = int(argv[1]) + c
      agent_name = 'agent_{}'.format(port)
      agent_dinheiro = randint(100,1000)
      agente_comprador = AgenteComprador(AID(name=agent_name), agent_dinheiro)
      agents.append(agente_comprador)
      c += 1000

  start_loop(agents)

if __name__ == '__main__':
  main()