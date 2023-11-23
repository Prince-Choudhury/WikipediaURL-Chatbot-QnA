import streamlit as st
from dotenv import load_dotenv
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from PIL import Image  
import wikipedia 
import base64
import requests
import pickle
import os


# Set page configuration
st.set_page_config(
    page_title="Wikipedia QnA",
    page_icon=Image.open("logo.png"),
    layout="wide",
)


# Add custom CSS for styling
app_css = """
    body {
        background-color: #f0f0f0;
    }
    .container {
        display: flex;
        align-items: center;
    }
    .logo-text {
        font-weight: bold;
        font-size: 40px;
        margin-left: 10px;
        color: #4e8cff; /* Set your desired color */
    }
    .logo-img {
        margin-right: 20px;
    }
    .col-container {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .iframe-container {
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .question-container {
        padding: 20px;
        margin-top: 10px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
"""

st.markdown(f'<style>{app_css}</style>', unsafe_allow_html=True)

# App Heading
st.markdown(
    """
    <div class="container">
        <img class="logo-img" src="data:image/png;base64,{0}" width=70 height=70>
        <p class="logo-text">Wikipedia QnA</p>
    </div>
    """.format(base64.b64encode(open("logo.png", "rb").read()).decode()),
    unsafe_allow_html=True,
)


# Load environment variables
load_dotenv()

def create_new_chat_session():
    # Function to create a new chat session and set it as active
    chat_id = len(st.session_state.chat_sessions) + 1
    session_key = f"Chat {chat_id}"
    st.session_state.chat_sessions[session_key] = []
    st.session_state.active_session = session_key

def initialize_chat_ui():
    if "active_session" in st.session_state:
        for message in st.session_state.chat_sessions[st.session_state.active_session]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    return st.chat_input("Ask Questions related to your article ")


# Sidebar contents
with st.sidebar:
    # Add a different chatbot symbol (emoji) next to the title
    st.title('🚀 WikiChatBot')

    # Add a short and engaging tagline for your application
    st.markdown('Your Intelligent Wikipedia Assistant')

    # Add a horizontal rule for separation
    st.markdown('---')

    st.markdown('Built with ❤️ by [Prince Choudhury](https://www.linkedin.com/in/prince-choudhury26/)')

    # Optionally, provide a link to your GitHub repository
    st.markdown('[GitHub Repo](https://github.com/Prince-Choudhury)')


def main():

    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}

    if "active_session" not in st.session_state:
        create_new_chat_session()

    # New Chat button
    if st.sidebar.button("New Chat"):
        create_new_chat_session()

    # Buttons for previous chat sessions
    for session in st.session_state.chat_sessions:
        if st.sidebar.button(session, key=session):  # Added a unique key
            st.session_state.active_session = session


    # Enter Your Link
    link = st.text_input('Enter the URL of the Wikipedia article:', value="", placeholder='https://en.wikipedia.org/wiki/Elon_Musk')
    if link:
        parsed_link = urlparse(link)
        response = requests.get(link)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text_content)

            # Use parsed link to get a suitable store name
            store_name = os.path.basename(parsed_link.path)

            if os.path.exists(f"{store_name}.pkl"):
                with open(f"{store_name}.pkl", "rb") as f:
                    vectorstore = pickle.load(f)
            else:
                embeddings = OpenAIEmbeddings()
                vectorstore = FAISS.from_texts(chunks, embedding=embeddings)
                with open(f"{store_name}.pkl", "wb") as f:
                    pickle.dump(vectorstore, f)

            # Chat UI and processing
            llm = OpenAI(temperature=0, max_tokens=1000)
            qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever())
            prompt = initialize_chat_ui()

            if prompt:
                st.session_state.chat_sessions[st.session_state.active_session].append({"role": "user", "content": prompt})  # Append the user input to the chat history
                with st.chat_message("user"):
                    st.markdown(prompt)  # Display the user input as a chat message
                    chat_history = st.session_state.chat_sessions.get(st.session_state.active_session, [])  # Get the chat history for the active session
                    result = qa({"question": prompt, "chat_history": [(msg["role"], msg["content"]) for msg in chat_history]})  # Get the answer from the conversational retrieval chain

                full_response = result["answer"]  # Get the answer text

                with st.chat_message("assistant"):
                    st.markdown(full_response)  # Display the answer as a chat message
                st.session_state.chat_sessions[st.session_state.active_session].append(
                    {"role": "assistant", "content": full_response})  # Append the answer to the chat history
                
if __name__ == '__main__':
    main()