class Model:
    def __init__(self, config):
        self.config = config

    def F(self, agent, agents):
        """Funkcja, która wywołuje przejścia stanów agentów."""
        agent.transition(agents, self.config)  # Agent samodzielnie zarządza swoim stanem
