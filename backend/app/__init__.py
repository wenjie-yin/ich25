from pydantic import BaseModel
from typing import List 

class WorldState(BaseModel):
    belief_vector: List[float]  # Level of belief for each node (0 to 1)
    connectivity_matrix: List[List[int]]  # Adjacency matrix for node connections
    current_message: str = ""