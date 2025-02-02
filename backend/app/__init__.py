from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class FeedEntry(BaseModel):
    message: str
    sender: Optional[int] = None
    timestamp: datetime = datetime.now()
    receiver: Optional[int] = None

class WorldState(BaseModel):
    belief_vector: List[float]  # Level of belief for each node (0 to 1)
    connectivity_matrix: List[List[float]]  # Adjacency matrix for node connections
    current_message: Optional[str] = None
    feed: List[FeedEntry] = []  # List of structured feed entries