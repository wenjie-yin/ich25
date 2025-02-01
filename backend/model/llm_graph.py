from backend.model.network import Network

class FeedEntry:

    def __init__(self, sentence, agent):
        self.sentence = sentence
        self.agent = agent


class LLMNetwork(Network):
    def __init__(self):
        pass

    def filter_feed(self, node):
        agents = {node.get_agent() for n in graph.get_adjacent(node)}
        return filter(lambda x: x.agent in agents, self.feed)

    def propagate_llm(self, sentence, user):
        self.feed.appendleft(FeedEntry(sentence, user.get_agent()))
        #iterate over nodes, filter feed for each one, send feed to llm api

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

