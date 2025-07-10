from typing import TypedDict
from langgraph.graph.message import add_messages
from src.data_classes import Profile

class State(TypedDict):
    file_path: str
    chunk_generator: object
    current_chunk: str
    last_profile: Profile | None

initial_state = {
    'file_path': 'resources/texts/نـادي المـوت_djvu.txt',
    'chunk_generator': None,
    'current_chunk': '',
    'last_profile': None,
}
