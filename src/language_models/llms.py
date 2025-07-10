from langchain.chat_models import init_chat_model

first_chunk_llm = init_chat_model('google_genai:gemini-2.5-flash', temperature=0.0)
other_chunk_llm = init_chat_model('google_genai:gemini-2.5-flash', temperature=0.0)
