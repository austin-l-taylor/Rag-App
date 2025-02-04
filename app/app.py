import streamlit as st
import functions, data_handler
import pandas as pd
import time
import os
from dotenv import load_dotenv

# Load the OpenAI API key from the .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")   

def clear_cache():
    st.cache_resource.clear()

def toggle_pdf_chat():
    st.session_state.pdf_chat = True
    clear_cache()

def detoggle_pdf_chat():
    st.session_state.pdf_chat = False
    clear_cache()

def render_expander():
    with st.expander("Need help?"):
        st.write(
            """
        This app is a chatbot that uses OpenAI's GPT model to generate responses to your messages.\n
        Please refresh the page if you wish to reset the chat history or swith to a different PDF.\n
        
        
        💡Models: Please selecte one of the models from the sidebar.\n
        - gpt-4o-mini: A smaller model that is faster and cheaper to use.\n
        - gpt-4o: A larger model that is more accurate and can generate more detailed responses.\n 
    
        💡Temperature: This parameter controls the randomness of the responses. A higher temperature will make the responses more creative and unpredictable.\n
        
        💡PDF Chat: If you have a PDF document, you can upload it to the app and ask questions about its content.\n
        """
        )

# Render the sidebar
def render_sidebar():
    """
    Summary: Renders the sidebar with the model selection, temperature slider, and PDF uploader.

    Returns:
        uploaded_file: The uploaded PDF
    """
    st.sidebar.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], key="openai_model") # Select the model
    st.sidebar.slider("Temperature", 0.0, 1.0, key="temperature") # Set the temperature
    st.sidebar.toggle("PDF Chat", key="pdf_chat", on_change=clear_cache) # Toggle the PDF chat

    uploaded_file = st.sidebar.file_uploader(
        "Upload a pdf file",
        key=st.session_state.pdf_uploader_key,
        type="pdf",
        on_change=toggle_pdf_chat
    )

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file

    return uploaded_file

def initialize_session_state():
    """
    Summary: Initializes the session state variables if they do not exist.
    """
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-4o-mini"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.0
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "pdf_uploader_key" not in st.session_state:
        st.session_state.pdf_uploader_key = "pdf_uploader"
    if "pdf_processed" not in st.session_state:
        st.session_state.pdf_processed = False
    if "pdf_chat" not in st.session_state:
        st.session_state.pdf_chat = False

def display_chat_history():
    """
    Summary: Displays the chat history in the chat message container.
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
def export_chat():
    """
    Summary: Exports the chat history to a CSV file.
    """
    # Convert the session state messages to a DataFrame
    messages_df = pd.DataFrame(st.session_state.messages)
    # Convert the DataFrame to a CSV string
    csv_data = messages_df.to_csv(index=False)

    # Create the download button with the CSV data
    st.download_button(
        label="Download Chat Log",
        data=csv_data,
        file_name="chat_log.csv",
        mime="text/csv",
    )
    
def basic_response_output(prompt):
    """
    Summary: Generates a response from ChatOpenAI and displays it in the chat message container.

    Args:
        prompt (str): The user message.
    """
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response from ChatOpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = functions.llm_response(
            api_key,
            prompt,
            current_model=st.session_state.openai_model,
            temperature=st.session_state.temperature,
        )
        response_content = response.content  # Access the content attribute directly

        # Simulate typing response
        for i in range(len(response_content)):
            full_response += str(response_content[i])
            message_placeholder.markdown(
                full_response + "❚"
            )  # Add a pipe character to simulate typing
            time.sleep(0.02)  # Adjust the delay to control typing speed

        message_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
    
def process_pdf(uploaded_file):
    """
    Summary: Processes the uploaded PDF file and creates a vector store from the text.

    Args:
        uploaded_file (File): The uploaded
    """
    try:
        with st.spinner("Processing PDF..."):
            documents = functions.get_pdf_text(uploaded_file)

            st.session_state.vector_store = functions.create_vectorstore_from_texts(
                documents, api_key=api_key, file_name=uploaded_file.name
            )
            st.session_state.pdf_processed = True
            st.success("PDF processed successfully!")
            

    except Exception as e:
        st.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

def pdf_response_output(prompt):   
    """
    Summary: Generates a response from ChatOpenAI and displays it in the chat message container.

    Args:
        prompt (str): The user message.
    """
    st.session_state.last_prompt = prompt
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.vector_store:
        # Generate answer
        with st.spinner("Generating answer..."):
            answer = functions.query_document(
                vectorstore=st.session_state.vector_store,
                query=prompt,
                api_key=api_key,
            )
        answer_content = answer.content

        # Display assistant message
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for i in range(len(answer_content)):
                full_response += str(answer_content[i])
                message_placeholder.markdown(full_response + "❚")
                time.sleep(0.02)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

def main():
    st.title("Welcome to the McKenney's AI Chatbot! 🤖")  

    initialize_session_state()
    uploaded_file = render_sidebar()
    render_expander()
    display_chat_history()
    
    prompt = st.chat_input("Hey 👋", key="main_input")
    
    if uploaded_file and st.session_state.pdf_processed == False:
        process_pdf(uploaded_file)
    if prompt and st.session_state.pdf_chat == True:
        pdf_response_output(prompt)
    if prompt and st.session_state.pdf_chat == False:
        basic_response_output(prompt)   
    if len(st.session_state.messages) > 0:
        messages = st.session_state.messages
        for message in messages:
            data_handler.push_chat_content(message)
        export_chat()
        data_handler.clear_db()
    
if __name__ == "__main__":
    main()