import graph
import server
import llm
import time
import json
import asyncio
from collections import deque

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
        self.timeout = 5
        self.num_agents = 2
        self.feed = deque(maxlength=self.num_agents)

    def propagate(self, sentence, user):
        for node in graph.get_adjacent(user):
            agent = node.get_agent()
            belief = llm.send_input(sentence, agent)
            graph.set_belief(node, belief)

    async def main_loop(self):
        while True:
            recv = asyncio.create_task(server.recv())
            done = await asyncio.wait({recv}, timeout=self.timeout)
            if recv in done:
                if recv.exit: break #TODO: if spread_belief takes a while might be nice to async waiting for this signal
                user = graph.get_user()
                self.propagate(recv.result(), user)
            graph.spread_belief()
            server.send(graph.serialise())

if name == "__main__":
    main = MainLoop()
    asyncio.run(main.main_loop())
