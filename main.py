from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dataclasses import dataclass


load_dotenv()

@dataclass
class Profile:
    name: str
    age: int
    role: str
    physical_characteristics: str
    personality: str
    events: list[str]
    relationships: list[str]


class State(TypedDict):
    profiles: Annotated[list[Profile], add_messages]
    chunks: Annotated[list[str], add_messages]
    porcessed_chunks: Annotated[list[str], add_messages]

FIRST_CHUNK_SYSTEM_PROMPT = '''You are an expert writer. Your primary function is to generate a list of profiles for literaty characters from a literature text.
                        Each profile should be a dict with a name, age, role in plot, physical_characteristics, personality, events, and relationships. the text is: {text}. Note: You should return a list of profiles in the following format: [{{'name': 'name', 'age': 'age', 'role': 'role', 'physical_characteristics': 'physical_characteristics', 'personality': 'personality', 'events': 'events', 'relationships': 'relationships'}}, ...]'''

OTHER_CHUNK_SYSTEM_PROMPT = '''You are an expert writer. Your primary function is to generate a list of profiles for literaty characters from a literature 
text based on a given list of profiles. Each profile should be a dict with a name, age, role in plot, physical_characteristics, personality, events, 
and relationships. You should combine the text with the profiles to generate a new list of profiles of the characters that 
has weren't part of the previous list of profiles and update the profiles that are already in the list based on the information of the text.
You should aim to keep the profiles summarized and concise, showing the core information for each character. the Text is: {text} and the profiles are: {profiles}. Note: You should return a list of profiles in the following format: [{{'name': 'name', 'age': 'age', 'role': 'role', 'physical_characteristics': 'physical_characteristics', 'personality': 'personality', 'events': 'events', 'relationships': 'relationships'}}, ...]'''

llm = init_chat_model('google_genai:gemini-2.5-flash')

def first_chunk_node(state: State):
    prompt = [HumanMessage(content=FIRST_CHUNK_SYSTEM_PROMPT.format(text=state['chunks'][0]))]
    return {'profiles': llm.invoke(prompt).content,
            'porcessed_chunks': state['porcessed_chunks'] + [state['chunks'][0]]}

def other_chunk_node(state: State):
    prompt = [HumanMessage(content=OTHER_CHUNK_SYSTEM_PROMPT.format(text=state['chunks'], profiles=state['profiles']))]
    return {'profiles': llm.invoke(prompt).content,
            'porcessed_chunks': state['porcessed_chunks'] + [state['chunks'][-1]]}

def router_node(state: State):
    return 'END' if len(state['porcessed_chunks']) == len(state['chunks']) else 'other_chunk'

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
config = {"configurable": {"thread_id": 1}}

initial_state = {
    'chunks': ['''Once upon a time in a land far, far away, there was a young woman named Alice. She was known for her curiosity and her love for adventure.
               One day, she decided to go on a journey to find the.''', '''The journey was long and full of challenges,Alice had to cross a dangerous forest, 
               navigate a treacherous river, and climb a towering mountain. Along the way, she met a wise old man who gave her a map and a compass. 
               With the map and compass, Alice was able to find her way and reach her destination.'''],
    'profiles': [],
    'porcessed_chunks': []
}

response = compiled_graph.invoke(initial_state, config=config)

print(response)