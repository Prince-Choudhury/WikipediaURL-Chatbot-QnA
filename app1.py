import streamlit as st  # Import the Streamlit module
from PIL import Image  # Import the Image class from the PIL module
import base64  # Import the base64 module to encode and decode images
import wikipedia  # Import the wikipedia module to access the Wikipedia API

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

# Main Content
col1, col2 = st.columns(2)  # Create two columns for the main content

# Wikipedia URL Input
with col1:  # Use the first column
    wiki_URL = st.text_input('Enter the URL of the Wikipedia article:', value="", placeholder='https://en.wikipedia.org/wiki/Elon_Musk')  # Create a text input for the Wikipedia URL
    if wiki_URL is not None and wiki_URL != "":  # Check if the URL is not empty
        st.markdown('<div class="iframe-container">', unsafe_allow_html=True)  # Add a div element for the iframe container
        st.components.v1.iframe(src=wiki_URL, width=None, height=550, scrolling=True)  # Display the Wikipedia page in an iframe
        st.markdown('</div>', unsafe_allow_html=True)  # Close the div element

# Question Input and Answers
with col2:  # Use the second column
    question = st.text_input('Ask questions related to your article:', value="", placeholder='What are Elon Musk\'s major contributions to the tech industry?')  # Create a text input for the question
    with st.spinner('Finding answer...'):  # Show a spinner while finding the answer
        if question is not None and question != "":  # Check if the question is not empty
            st.markdown('<div class="question-container">', unsafe_allow_html=True)  # Add a div element for the question container
            html_answers = wikipedia.get_html_answers(question, wiki_URL, 3)  # Get the HTML answers from the wikipedia module
            st.components.v1.html(html=html_answers, width=None, height=550, scrolling=True)  # Display the HTML answers in a component
            st.markdown('</div>', unsafe_allow_html=True)  # Close the div element
