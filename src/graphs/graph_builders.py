from langgraph.graph import StateGraph, START, END
from src.states import State
from src.graphs.nodes import chunker_generator_node, first_chunk_node, other_chunk_node, router_node

graph = StateGraph(State)

graph.add_node('chunker_generator', chunker_generator_node)
graph.add_node('first_chunk', first_chunk_node)
graph.add_node('other_chunk', other_chunk_node)

graph.set_entry_point('chunker_generator')
graph.add_edge('chunker_generator', 'first_chunk')
graph.add_conditional_edges(
    'first_chunk',
    router_node,
    {
        'other_chunk': 'other_chunk',
        'END': END
    }
)
graph.add_conditional_edges(
    'other_chunk',
    router_node,
    {
        'other_chunk': 'other_chunk',
        'END': END
    }
)

compiled_graph = graph.compile()