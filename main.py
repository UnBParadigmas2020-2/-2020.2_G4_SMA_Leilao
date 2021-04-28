from agentes.agent_example_1 import AgenteHelloWorld
from pade.misc.utility import start_loop
from pade.acl.aid import AID
from sys import argv

if __name__ == '__main__':
    agents_per_process = 3
    c = 0
    agents = list()
    for i in range(agents_per_process):
        port = int(argv[1]) + c
        agent_name = 'agent_hello_{}@localhost:{}'.format(port, port)
        agente_hello = AgenteHelloWorld(AID(name=agent_name))
        agents.append(agente_hello)
        c += 1000

    start_loop(agents)