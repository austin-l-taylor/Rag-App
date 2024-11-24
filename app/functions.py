from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

import os
import tempfile
import re

def llm_response(api_key, user_question, current_model, temperature):
    """Receives a user question and returns a response from the language model.

    Args:
        api_key : users OpenAI API key
        user_question (string): The question asked by the user
    """
    
    llm = ChatOpenAI(model=current_model, api_key=api_key, temperature=temperature)
    llm_response = llm.invoke(user_question)

    return llm_response


def clean_filename(filename):
    """
    Clean the filename by removing the "(number)" pattern.

    Parameters:
        filename (str): The filename to clean

    Returns:
        str: The cleaned filename
    """
    # Regular expression to find "(number)" pattern
    new_filename = re.sub(r"\s\(\d+\)", "", filename)
    return new_filename


def get_pdf_text(uploaded_file):
    """
    Load a PDF document from an uploaded file and return it as a list of documents

    Parameters:
        uploaded_file (file-like object): The uploaded PDF file to load

    Returns:
        list: A list of documents created from the uploaded PDF file
    """

    temp_file = None

    try:
        # Step 1
        # Read file content
        input_file = uploaded_file.read()

        # Create a temporary file (PyPDFLoader requires a file path to read the PDF,
        # it can't work directly with file-like objects or byte streams that we get from Streamlit's uploaded_file)
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(input_file)
        temp_file.close()

        # load PDF document
        loader = PyPDFLoader(temp_file.name)
        documents = loader.load()

        return documents

    finally:
        # Ensure the temporary file is deleted when we're done with it
        if temp_file is not None:
            os.unlink(temp_file.name)


def split_document(documents, chunk_size, chunk_overlap):
    """
    Function to split generic text into smaller chunks.
    chunk_size: The desired maximum size of each chunk (default: 400)
    chunk_overlap: The number of characters to overlap between consecutive chunks (default: 20).

    Returns:
        list: A list of smaller text chunks created from the generic text
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " "],
    )

    return text_splitter.split_documents(documents)


def get_embedding_function(api_key):
    """
    Return an OpenAIEmbeddings object, which is used to create vector embeddings from text.
    The embeddings model used is "text-embedding-ada-002" and the OpenAI API key is provided
    as an argument to the function.

    Parameters:
        api_key (str): The OpenAI API key to use when calling the OpenAI Embeddings API.

    Returns:
        OpenAIEmbeddings: An OpenAIEmbeddings object, which can be used to create vector embeddings from text.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", api_key=api_key)
    return embeddings


def create_vectorstore(chunks, embedding_function, file_name, vector_store_path="db"):
    """
    Create a vector store from a list of text chunks.

    :param chunks: A list of generic text chunks
    :param embedding_function: A function that takes a string and returns a vector
    :param file_name: The name of the file to associate with the vector store
    :param vector_store_path: The directory to store the vector store

    :return: A Chroma vector store object
    """
    print("Creating vector store...")

    try:
        # Debugging: Print the number of chunks and the first chunk
        print(f"Number of chunks: {len(chunks)}")
        
        # Create a new Chroma database from the documents
        vectorstore = Chroma.from_documents(
            documents=chunks,
            collection_name=clean_filename(file_name),
            embedding=embedding_function,
            persist_directory=vector_store_path,
        )
        print("Vector store created successfully.")
    except Exception as e:
        print(f"An error occurred while creating the vector store: {e}")
        raise

    return vectorstore

def create_vectorstore_from_texts(documents, api_key, file_name):
    """
    Create a vector store from a list of texts.

    :param documents: A list of generic text documents
    :param api_key: The OpenAI API key used to create the vector store
    :param file_name: The name of the file to associate with the vector store

    :return: A Chroma vector store object
    """
    # Step 2 split the documents
    docs = split_document(documents, chunk_size=1000, chunk_overlap=200)
    print("Step 2: Split the documents")

    # Step 3 define embedding function
    embedding_function = get_embedding_function(api_key)
    print("Step 3: Define embedding function")

    # Step 4 create a vector store
    vectorstore = create_vectorstore(docs, embedding_function, file_name)
    print("Step 4: Create a vector store")

    return vectorstore


# Prompt template
PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer
the question. If you don't know the answer, say that you
don't know. DON'T MAKE UP ANYTHING.

{context}

---

Answer the question based on the above context: {question}
"""


def format_docs(docs):
    """
    Format a list of Document objects into a single string.

    :param docs: A list of Document objects

    :return: A string containing the text of all the documents joined by two newlines
    """
    return "\n\n".join(doc.page_content for doc in docs)

def query_document(vectorstore, query, api_key):
    """
    Query a vector store with a question and return a plain response.

    :param vectorstore: A Chroma vector store object
    :param query: The question to ask the vector store
    :param api_key: The OpenAI API key to use when calling the OpenAI Embeddings API

    :return: A plain response from the language model
    """
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)

    retriever = vectorstore.as_retriever(search_type="similarity")

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_template
        | llm
    )

    response = rag_chain.invoke(query)
    return response
