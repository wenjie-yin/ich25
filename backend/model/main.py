import time
import json
import asyncio
import threading
from app import WorldState
from model.network import Network
from app import FeedEntry
from datetime import datetime

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
        self.update_delay = 4
        self.n_nodes = 10
        # Change to async lock
        self.update_lock = asyncio.Lock()

        # Initialise network
        self.network = Network(self.n_nodes, belief="The COVID-19 vaccine is harmful to humans.")

        # Exit flag
        self.terminate = False
        self._task = None
        self._loop = None

    def __enter__(self):
        """Start the game loop in a new event loop in a separate thread"""
        self.terminate = False
        
        def run_async_loop():
            asyncio.run(self.game_loop())

        self._thread = threading.Thread(target=run_async_loop)
        self._thread.daemon = True
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up when exiting the context"""
        self.terminate = True
        if self._loop:
            self._loop.call_soon_threadsafe(self._loop.stop)
        if self._thread:
            self._thread.join()

    async def game_loop(self):
        """Async game loop"""
        while not self.terminate:
            async with self.update_lock:
                await self.network.update_with_agent_crosstalk()
            await asyncio.sleep(self.update_delay)

    async def send_user_message(self, msg: str):
        """Send message from user to update network"""
        async with self.update_lock:
            await self.network.update_with_user_input(msg)

    def get_world_state(self) -> WorldState:
        matrix, beliefs = self.network.serialise()
        feed = [FeedEntry(message=entry.message, sender=entry.node_index, timestamp=entry.timestamp) for entry in self.network.feed]
        return WorldState(
            belief_vector=beliefs,
            connectivity_matrix=matrix,
            feed=feed # Include feed in world state
        )
