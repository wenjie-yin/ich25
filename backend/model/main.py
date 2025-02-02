import time
import json
import asyncio
import threading
from app import WorldState
from model.network import Network

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

        # Exit flag
        self.terminate = False
        self._thread = None

    def __enter__(self):
        """Start the game loop in a separate thread when entering the context"""
        self.terminate = False
        self._thread = threading.Thread(target=self.game_loop)
        self._thread.daemon = True  # Make thread daemon so it exits when main thread exits
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when exiting the context"""
        self.terminate = True
        if self._thread:
            self._thread.join()

    def game_loop(self):
        while not self.terminate:
            time.sleep(self.update_delay)
            #TODO: make async
            # self.network.update_with_random_interaction()
            # self.network.update_with_agent_crosstalk()

    async def send_user_message(self, msg: str):
        """Send message from user to update network
        """
        self.network.update_with_user_input(msg)

    def get_world_state(self) -> WorldState:
        matrix, beliefs = self.network.serialise()
        return WorldState(
            belief_vector=beliefs,
            connectivity_matrix=matrix,
        )
