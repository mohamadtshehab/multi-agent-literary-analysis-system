from langgraph.graph import StateGraph, START, END
from src.schemas.states import State
from src.graphs.nodes import chunker, name_querier, profile_retriever_creator, profile_refresher, chunk_updater, router_to_name_querier_or_end, router_to_profile_retriever_creator_or_chunk_updater

graph = StateGraph(State)

graph.add_node('chunker', chunker)
graph.add_node('name_querier', name_querier)
graph.add_node('profile_retriever_creator', profile_retriever_creator)
graph.add_node('profile_refresher', profile_refresher)
graph.add_node('chunk_updater', chunk_updater)


graph.set_entry_point('chunker')
graph.add_edge('chunker', 'chunk_updater')

graph.add_conditional_edges('chunk_updater', router_to_name_querier_or_end, {
    'name_querier': 'name_querier',
    'END': END
})

graph.add_conditional_edges(
    'name_querier',
    router_to_profile_retriever_creator_or_chunk_updater,
    {
        'profile_retriever_creator': 'profile_retriever_creator',
        'chunk_updater': 'chunk_updater',
    }
)


graph.add_edge('profile_retriever_creator', 'profile_refresher')

graph.add_edge('profile_refresher', 'chunk_updater')

compiled_graph = graph.compile()