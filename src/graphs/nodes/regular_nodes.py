from src.language_models.prompts import name_query_prompt, profile_update_prompt, summary_prompt
from src.language_models.llms import name_query_llm, profile_update_llm, summary_llm
from src.schemas.states import State
from src.preprocessors.text_splitters import TextChunker
from src.preprocessors.text_cleaners import clean_arabic_text_comprehensive
from src.databases.database import character_db
from src.schemas.data_classes import Profile
import os

def cleaner(state: State):
    """
    Node that cleans the text from the file before chunking.
    Uses the clean_text function to normalize and clean the input text.
    """
    file_path = state['file_path']
    
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        raw_text = file.read()

    # Clean the text using the clean_text function
    cleaned_text = clean_arabic_text_comprehensive(raw_text)
    
    return {
        'cleaned_text': cleaned_text
    }


def chunker(state: State):
    """
    Node that takes the cleaned text from the state and yields chunks using a generator for memory efficiency.
    Only the current chunk is kept in the state.
    """
    cleaned_text = state['cleaned_text']
    
    if not cleaned_text:
        raise ValueError("No cleaned text available in state")
        
    chunker = TextChunker(chunk_size=5000, chunk_overlap=200)
    
    chunks = chunker.chunk_text_arabic_optimized(cleaned_text)
    
    def chunk_generator():
        for chunk in chunks:
            yield chunk
            
    gen = chunk_generator()
        
    return {
        'chunk_generator': gen,
    }
    
    
def first_name_querier(state: State):
    """
    Node that queries the name of the character in the current chunk.
    """
    third_of_length_of_previous_chunk = len(state['previous_chunk'])//3
    
    context = str(state['previous_chunk'][2 * third_of_length_of_previous_chunk:]) + " " + str(state['current_chunk'])
    
    chain_input = {
        "text": str(context)
    }
    
    chain = name_query_prompt | name_query_llm
    
    response = chain.invoke(chain_input)
    
    characters = response.characters if hasattr(response, 'characters') else []
    
    return {
        'last_appearing_characters': characters
    } 
    
def second_name_querier(state: State):
    """
    Node that queries the name of the character in the last summary.
    """
    context = state['last_summary']
    
    chain_input = {
        "text": str(context)
    }
    
    chain = name_query_prompt | name_query_llm
    
    response = chain.invoke(chain_input)
    
    characters = response.characters if hasattr(response, 'characters') else []
    
    return {
        'last_appearing_characters': characters
    } 


def profile_retriever_creator(state: State):
    """
    Node that creates a new profile or retrieves an existing one.
    Uses last_appearing_characters to retrieve profiles from character_db. If no character exists,
    creates a new entry with that name and hint, keeping other profile data null.
    """
    last_appearing_characters = state['last_appearing_characters']
    
    profiles = []
    
    for character in last_appearing_characters:
        name = character.name
        hint = character.hint
        
        existing_characters = character_db.find_characters_by_name(name)
        
        if existing_characters:
            # create the data dictionary that will be send to the LLM
            for char in existing_characters:
                profile_data = char['profile']
                profile = Profile(
                    name=char['name'],
                    hint=profile_data['hint'],
                    age=profile_data['age'],
                    role=profile_data['role'],
                    physical_characteristics=profile_data['physical_characteristics'],
                    personality=profile_data['personality'],
                    events=profile_data['events'],
                    relationships=profile_data['relationships'],
                    aliases=profile_data['aliases'],
                    id=char['id']
                )
                profiles.append(profile)
        else:
            # create the json object that will be stored in the database (no need for id because it has its own column)
            new_profile = {
                'name': name,
                'hint': hint,
                'age': '',
                'role': '',
                'physical_characteristics': [],
                'personality': '',
                'events': [],
                'relationships': [],
                'aliases': [],
            }
            
            character_db.insert_character(name, new_profile)
            
            # Create data dictionary that will be send to the LLM
            profile = Profile(
                name=name,
                hint=hint,
                age='',
                role='',
                physical_characteristics=[],
                personality='',
                events=[],
                relationships=[],
                aliases=[],
                id='',
            )
            profiles.append(profile)
    
    return {'last_profiles': profiles}


def profile_refresher(state: State):
    """
    Node that refreshes the profiles based on the current chunk.
    """
    chain_input = {
        "text": str(state['last_summary']),
        "profiles": str(state['last_profiles'])
    }
    chain = profile_update_prompt | profile_update_llm
    response = chain.invoke(chain_input)
    
    # Extract profiles from the structured output
    updated_profiles = []
    for profile_data in response.profiles:
        # create the data dictionary that will be an item in the list of profiles in the state
        profile = Profile(
            name=profile_data.name,
            hint=profile_data.hint,
            age=profile_data.age,
            role=profile_data.role,  # Use the role determined by the LLM with tool
            physical_characteristics=profile_data.physical_characteristics,
            personality=profile_data.personality,
            events=profile_data.events,
            relationships=profile_data.relations,
            aliases=profile_data.aliases,
            id=profile_data.id
        )
        updated_profiles.append(profile)
        
        # create the json object that will be updated in the database
        updated_profile_dict = {
            'name': profile_data.name,
            'hint': profile_data.hint,
            'age': profile_data.age,
            'role': profile_data.role,  # Use the role determined by the LLM with tool
            'physical_characteristics': profile_data.physical_characteristics,
            'personality': profile_data.personality,
            'events': profile_data.events,
            'relationships': profile_data.relations,
            'aliases': profile_data.aliases,
        }
    
        character_db.update_character(
            profile_data.id,
            updated_profile_dict
        )
    
    return {
        'last_profiles': updated_profiles,
    }

def chunk_updater(state: State):
    """
    Node that updates the previous and current chunks in the state.
    """
    try:
        current_chunk = next(state['chunk_generator'])
        return {
            'previous_chunk': state.get('current_chunk', ''),
            'current_chunk': current_chunk,
            'no_more_chunks': False
        }
    except StopIteration:
        return {'no_more_chunks': True}

    

def summarizer(state: State):
    """
    Node that summarizes the text based on the profiles.
    """
    third_of_length_of_last_summary = len(state['last_summary'])//3
    context = str(state['last_summary'][2 * third_of_length_of_last_summary:]) + " " + str(state['current_chunk'])
    chain_input = {
        "text": context,
        "names": str(state['last_appearing_characters'])
    }
    chain = summary_prompt | summary_llm
    response = chain.invoke(chain_input)
    
    return {'last_summary': response.summary}