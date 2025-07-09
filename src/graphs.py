from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.states import State
from src.nodes import first_chunk_node, other_chunk_node, router_node

graph = StateGraph(State)

graph.add_node('first_chunk', first_chunk_node)
graph.add_node('other_chunk', other_chunk_node)

graph.add_edge(START, 'first_chunk')
graph.add_edge('first_chunk', 'other_chunk')
graph.add_conditional_edges(
    'other_chunk',
    router_node,
    {
        'other_chunk': 'other_chunk',
        'END': END
    }
)
graph.add_edge('other_chunk', END)


checkpointer = MemorySaver()
compiled_graph = graph.compile(checkpointer=checkpointer)