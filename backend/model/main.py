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
        self.network = Network(self.n_nodes, belief="The COVID-19 vaccine is harmful to humans.")
        self.terminate = False
        self._task = None
        self.update_lock = None  # Will be created in the event loop

    async def _init_lock(self):
        """Initialize the lock in the correct event loop"""
        self.update_lock = asyncio.Lock()

    async def game_loop(self):
        """Async game loop"""
        await self._init_lock()  # Initialize lock in the correct loop
        while not self.terminate:
            async with self.update_lock:
                await self.network.update_with_agent_crosstalk()
                self.network.cluster()
            await asyncio.sleep(self.update_delay)

    async def send_user_message(self, msg: str):
        """Send message from user to update network"""
        if self.update_lock is None:
            await self._init_lock()
            
        async with self.update_lock:
            await self.network.update_with_user_input(msg)
            self.network.cluster()

    def get_world_state(self) -> WorldState:
        matrix, beliefs = self.network.serialise()
        feed = [FeedEntry(message=entry.message, sender=entry.node_index, timestamp=entry.timestamp) 
               for entry in self.network.feed]
        return WorldState(
            belief_vector=beliefs,
            connectivity_matrix=matrix,
            feed=feed
        )
