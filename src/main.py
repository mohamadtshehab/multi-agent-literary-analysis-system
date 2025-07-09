from dotenv import load_dotenv
from src.graphs import compiled_graph
from src.states import initial_state
from src.configs import config

load_dotenv()

response = compiled_graph.invoke(initial_state, config=config)

if __name__ == "__main__":
    print(response)