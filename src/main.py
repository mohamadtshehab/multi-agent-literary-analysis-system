from dotenv import load_dotenv
from src.graphs import compiled_graph
from src.states import initial_state


load_dotenv()

config = {"configurable": {"thread_id": 1}}

response = compiled_graph.invoke(initial_state, config=config)

if __name__ == "__main__":
    print(response)