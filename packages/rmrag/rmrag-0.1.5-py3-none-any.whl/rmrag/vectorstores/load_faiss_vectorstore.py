from dotenv import load_dotenv
load_dotenv()
from typing import Type, Union
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_faiss_vectorstore(vectorstore_folder:str='./vectorstore/', embedding_model:Type[Union[HuggingFaceEmbeddings, OpenAIEmbeddings]] = HuggingFaceEmbeddings, specific_model:str='intfloat/multilingual-e5-large') -> FAISS:
    """  
    Description:
    Loads a local FAISS vectorstore

    Remember to have a .env file in the working directory with API keys for HuggingFace and OpenAI.

    Args: 
        vectorstore_folder: folder where the 'index.faiss' file is located. Defaults to './vectorstore/'.
        embedding_model: Must be HuggingFaceEmbeddings or OpenAIEmbeddings. Defaults to HuggingFaceEmbeddings.
        specific_model: For example 'sentence-transformers/all-MiniLM-L6-v2' or 'text-embedding-3-small'. Defaults to 'intfloat/multilingual-e5-large'.

    Returns:
        A FAISS vectorstore object.
    """
   
    # Validate that the embedding_model is either HuggingFaceEmbeddings or OpenAIEmbeddings
    if not issubclass(embedding_model, (HuggingFaceEmbeddings, OpenAIEmbeddings)):
        raise ValueError("embedding_model must be either HuggingFaceEmbeddings or OpenAIEmbeddings")
    
    try:
        # Instantiate embeddings based on the provided embedding model type
        if issubclass(embedding_model, HuggingFaceEmbeddings):
            embeddings = embedding_model(model_name=specific_model, show_progress=True)
        elif issubclass(embedding_model, OpenAIEmbeddings):
            embeddings = embedding_model(model=specific_model, show_progress=True)

        print("Embeddings defined successfully.")
    except Exception as e:
        print("Error defining embeddings:", e)
        return # Stop execution if embeddings cannot be created

    try: 
        # Load the local FAISS vectorstore
        vectorstore = FAISS.load_local(vectorstore_folder, embeddings, allow_dangerous_deserialization=True)
        print("Vectorstore loaded successfully.")
        return vectorstore
    except Exception as e:
        print("Error loading vectorstore index: ", e)
        return