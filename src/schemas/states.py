from typing import TypedDict
from langgraph.graph.message import add_messages
from src.databases.database import CharacterDatabase
from src.schemas.data_classes import Profile, LastAppearingCharacter

class State(TypedDict):
    file_path: str
    cleaned_text: str
    context_text: str
    chunk_generator: object
    current_chunk: str
    previous_chunk: str
    last_profiles: list[Profile] | None
    last_appearing_characters: list[LastAppearingCharacter] | None
    database: CharacterDatabase
    no_more_chunks: bool
    is_arabic : bool
    last_summary: str

initial_state = {
    'file_path': 'resources/texts/english-test.txt',
    'cleaned_text': '',
    'context_text': '',
    'chunk_generator': None,
    'current_chunk': '',
    'previous_chunk': '',
    'last_profiles': None,
    'last_appearing_characters': None,
    'database': CharacterDatabase(),
    'no_more_chunks': False,
    'last_summary': ''
}
