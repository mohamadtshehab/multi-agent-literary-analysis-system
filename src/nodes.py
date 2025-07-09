from src.prompts import first_chunk_prompt, other_chunk_prompt
from src.llms import first_chunk_llm, other_chunk_llm
from src.states import State

def first_chunk_node(state: State):

    chain = first_chunk_prompt | first_chunk_llm
    model_input = {
        "text": str(state['chunks'][0].content)
    }
    response = chain.invoke(model_input)
    dict = {
        'profiles': response,
        'porcessed_chunks': state['chunks'][0]
    }
    
    return dict

def other_chunk_node(state: State):
    
    chain = other_chunk_prompt | other_chunk_llm
    model_input = {
        "text": str(state['chunks'][-1].content), 
        "profiles": str(state['profiles'][-1])
    }
    response = chain.invoke(model_input)
    dict = {
        'profiles': response,
        'porcessed_chunks': state['porcessed_chunks'] + [state['chunks'][-1]]
    }
    
    return dict

def router_node(state: State):
    return 'END' if len(state['porcessed_chunks']) == len(state['chunks']) else 'other_chunk'
