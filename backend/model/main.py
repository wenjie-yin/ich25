import graph
import server
import llm
import time
import json
import asyncio
from backend.model.network import Network

"""
initialise: n agents with random belief states and one player in graphs with adjacent connections (fully connected for now)
on input: query adjacent agents -> propegate graph
loop:
check for input
tick graph every so often

objects:
graph: agents, edges
agent: beliefes, LLM key
feed: list of LLM outputs (later)

functions:
main
tick_graph:
    for each agent, communicate with adjacents to spread belief states (later update connections)
spread_belief:
    either statistical or LLM API
    update node belief values
propegate_graph:
    propegate user impact
"""



class MainLoop:

    def __init__(self):
        self.update_delay = 1
        self.n_nodes = 10

        # Initialise network
        self.network = Network(self.n_nodes, belief="The earth is flat")

        # Exit 
        self.terminate = False

    def game_loop(self):
        while not self.terminate:
            time.sleep(self.update_delay)
            self.network.update_with_agent_crosstalk()
    
    def send_user_message(self, msg: str):
        """Send message from user to update network
        """
        pass

    """
    async def main_loop(self):
        while not self.terminate:
            recv = asyncio.create_task(server.recv())
            done = await asyncio.wait({recv}, timeout=self.timeout)
            if recv in done:
                if recv.exit: #TODO: if spread_belief takes a while might be nice to async waiting for this signal
                    user = graph.get_user()
                    self.propagate(recv.result(), user)
            graph.spread_belief()
            server.send(graph.serialise())
    """


if name == "__main__":
    main = MainLoop()
    asyncio.run(main.main_loop())
