# Wikipedia QnA Chatbot

An intelligent Wikipedia assistant that allows users to chat with Wikipedia articles using natural language questions.

![Wikipedia QnA Logo](logo.png)

## Features

- Interactive chat interface for querying Wikipedia articles
- Support for any Wikipedia article via URL input
- Multiple chat sessions for different articles
- Semantic search using vector embeddings
- Conversational memory to maintain context in discussions
- Clean and intuitive user interface

## How It Works

1. Enter a Wikipedia article URL in the input field
2. The application extracts and processes the article content
3. Ask questions about the article in natural language
4. Get accurate answers based on the article content
5. Create multiple chat sessions to explore different articles

## Technical Details

This application uses:
- **Streamlit**: For the web interface
- **LangChain**: For conversational retrieval chain
- **FAISS**: For efficient vector storage and similarity search
- **OpenAI Embeddings**: To convert text into vector representations
- **BeautifulSoup**: For web scraping Wikipedia articles
- **Pickle**: For storing and retrieving vector databases

## Requirements

- Python 3.7+
- OpenAI API key
- Required Python packages:
  - streamlit
  - streamlit-extras
  - langchain
  - openai
  - faiss-cpu
  - beautifulsoup4
  - requests
  - python-dotenv
  - pillow
  - wikipedia-api

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Prince-Choudhury/WikipediaURL-Chatbot-QnA.git
   cd WikipediaURL-Chatbot-QnA
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

1. Make sure you have the `logo.png` file in the project directory
2. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
3. Open your browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)
4. Enter a Wikipedia article URL in the input field
5. Start asking questions about the article

## Project Structure

- `app.py`: Main application file containing the Streamlit interface and Wikipedia QnA functionality
- `logo.png`: Logo image for the application
- `.env`: Environment file for storing API keys (not included in repository)
- `*.pkl`: Generated vector stores for each Wikipedia article (created at runtime)

## How to Use

1. **Enter a Wikipedia URL**: Paste a full Wikipedia article URL in the input field
2. **Ask Questions**: Type your questions in the chat input at the bottom
3. **Create New Chats**: Click the "New Chat" button in the sidebar to start a fresh conversation
4. **Switch Between Chats**: Click on any previous chat session in the sidebar to continue that conversation

## Performance Notes

- The first time you load an article, it may take a few moments to process and create the vector store
- Subsequent queries to the same article will be faster as the vector store is saved locally
- For very large articles, processing time may be longer

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Built with ❤️ by [Prince Choudhury](https://www.linkedin.com/in/prince-choudhury26/)

