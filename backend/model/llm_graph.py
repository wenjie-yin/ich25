from backend.model.network import Network


class LLMNetwork(Network):
    def __init__(self):
        pass
    
    def get_adjacent(self, node):
        raise NotImplementedError

    def get_belief(self, node):
        """Get belief state of node
        Args:
            node : Node object
        """
        raise NotImplementedError
    
    def set_belief(self, node, belief):
        """Set belief state of node
        Args:
            node: Node object
            belief (float): Belief level
        """
        raise NotImplementedError
    
    def serialise(self):
        raise NotImplementedError
    
    def spread_belief(self):
        raise NotImplementedError

