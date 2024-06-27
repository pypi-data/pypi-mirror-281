from typing import Union
from dotenv import load_dotenv
import os
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def create_embeddings_and_faiss_vectorstore(chunks: list, embedding_provider: str = 'HuggingFaceEmbeddings', specific_model: str = 'intfloat/multilingual-e5-large') -> FAISS:
    """
    Description:
    Embeds the text chunks and saves it in a vectorstore.

    Remember to have a .env file in the working directory with API keys for HuggingFace and OpenAI.

    Args:
        chunks: A list of chunks from a Langchain loader.
        embedding_model: Must be 'HuggingFaceEmbeddings' or 'OpenAIEmbeddings'. Defaults to 'HuggingFaceEmbeddings'.
        specific_model: For example 'sentence-transformers/all-MiniLM-L6-v2' or 'gpt-3.5-turbo'. Defaults to 'intfloat/multilingual-e5-large'.

    Returns:
        None. It saves a FAISS vectorstore in a folder called 'vectorstore' in the current working directory.
    """
    # Map string input to the actual class
    embedding_providers = {
        'HuggingFaceEmbeddings': HuggingFaceEmbeddings,
        'OpenAIEmbeddings': OpenAIEmbeddings
    }

    if embedding_provider not in embedding_providers:
        raise ValueError("embedding_model must be either 'HuggingFaceEmbeddings' or 'OpenAIEmbeddings'")

    embedding_provider = embedding_providers[embedding_provider]

    try:
        embeddings = embedding_provider(model_name=specific_model, show_progress=True)
        print("Embeddings created")
    except Exception as e:
        print("Error creating embeddings:", e)
        return  # Stop execution if embeddings cannot be created

    try:
        os.makedirs('./vectorstore', exist_ok=True)
        
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local('./vectorstore/')
        print("Vectorstore created")
    except Exception as e:
        print("Error creating vectorstore:", e)
