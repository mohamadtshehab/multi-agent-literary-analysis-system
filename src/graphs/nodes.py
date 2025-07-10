from src.language_models.prompts import first_chunk_prompt, other_chunk_prompt
from src.language_models.llms import first_chunk_llm, other_chunk_llm
from src.states import State

def chunker_generator_node(state: State):
    """
    Node that takes the file path from the state and yields chunks using a generator for memory efficiency.
    Only the current chunk is kept in the state.
    """
    from src.preprocessors.text_splitters import TextChunker
    import os
    file_path = state['file_path']
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
    chunks = chunker.chunk_text_arabic_optimized(text)
    def chunk_generator():
        for chunk in chunks:
            yield chunk
    gen = chunk_generator()
    try:
        first_chunk = next(gen)
    except StopIteration:
        first_chunk = ''
    return {
        'file_path': file_path,
        'chunk_generator': gen,
        'current_chunk': first_chunk,
        'last_profile': None
    }

def first_chunk_node(state: State):
    """
    Node that processes the first chunk from the generator and stores only the current chunk and last profile.
    """
    chain = first_chunk_prompt | first_chunk_llm
    model_input = {
        "text": str(state['current_chunk'])
    }
    response = chain.invoke(model_input)
    return {
        'file_path': state['file_path'],
        'chunk_generator': state['chunk_generator'],
        'current_chunk': state['current_chunk'],
        'last_profile': response
    }

def other_chunk_node(state: State):
    """
    Node that processes the next chunk from the generator and stores only the current chunk and last profile.
    """
    gen = state['chunk_generator']
    try:
        next_chunk = next(gen)
    except StopIteration:
        next_chunk = ''
    if not next_chunk:
        return {
            'file_path': state['file_path'],
            'chunk_generator': None,
            'current_chunk': '',
            'last_profile': state['last_profile']
        }
    chain = other_chunk_prompt | other_chunk_llm
    model_input = {
        "text": str(next_chunk),
        "profiles": str(state['last_profile'])
    }
    response = chain.invoke(model_input)
    return {
        'file_path': state['file_path'],
        'chunk_generator': gen,
        'current_chunk': next_chunk,
        'last_profile': response
    }

def router_node(state: State):
    # End if generator is None or current_chunk is empty
    if state['chunk_generator'] is None or not state['current_chunk']:
        return 'END'
    else:
        return 'other_chunk'
