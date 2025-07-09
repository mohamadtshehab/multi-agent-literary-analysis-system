from dotenv import load_dotenv
from src.graphs import compiled_graph
from src.states import initial_state
from src.configs import config
from src.visualize_graph import visualize_graph

load_dotenv()

if __name__ == "__main__":
    visualize_graph(compiled_graph)
    # response = compiled_graph.invoke(initial_state, config=config)
    # print(response)