from src.schemas.states import State

def router_from_language_checker_to_cleaner_or_end(state : State):
    """
     Node that routes to the cleaner or end based on the response from the language checker.
    """
    if state["is_arabic"]:
        return "cleaner"
    else:
        return "END"
    
    
def router_from_chunker_to_first_name_querier_or_end(state: State):
    """
    Node that routes to the name querier or end based on the response from the chunker.
    """
    if state['no_more_chunks']:
        return 'END'
    else:
        return 'first_name_querier'
    
    
def router_from_first_name_querier_to_summarizer_or_chunk_updater(state: State):
    """
    Node that routes to the summarizer or chunk updater based on the response from the first name querier.
    """
    if state['last_appearing_characters']:
        return 'summarizer'
    else:
        return 'chunk_updater'