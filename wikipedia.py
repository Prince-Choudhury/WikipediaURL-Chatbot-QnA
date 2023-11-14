import requests  # Import the requests module to send HTTP requests
from bs4 import BeautifulSoup  # Import the BeautifulSoup class from the bs4 module to parse HTML content
import re  # Import the re module to use regular expressions
import pandas as pd  # Import the pandas module to manipulate data frames

from transformers import pipeline  # Import the pipeline function from the transformers module to create a question-answering pipeline

def get_soup(url):
    # Function to get the soup object from a given URL
    # Page content from Website URL
    page = requests.get(url)  # Send a GET request to the URL and get the response
    
    # parse html content
    soup = BeautifulSoup(page.content , 'html.parser')  # Parse the HTML content of the response using BeautifulSoup

    return soup  # Return the soup object

def clean_wiki_content(text):
    # Function to clean the Wikipedia content from unwanted characters
    text = re.sub("\[\d+\]", "" , text)  # Remove the citation numbers in square brackets using regular expressions
    text = text.replace("[edit]", "")  # Remove the "[edit]" string

    return text  # Return the cleaned text

def get_paragraph_text(p):
    # Function to get the paragraph text from a p tag
    paragraph_text = ''  # Initialize an empty string
    for tag in p.children:  # Loop through the children tags of the p tag
        paragraph_text = paragraph_text + tag.text  # Append the text of each child tag to the paragraph text
    
    return paragraph_text  # Return the paragraph text

def get_wiki_extract(url):
    # Function to get the Wikipedia extract from a given URL
    soup = get_soup(url)  # Get the soup object from the URL
    headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']  # Define a list of header tags
    wiki_extract = []  # Initialize an empty list
    for tag in soup.find_all():  # Loop through all the tags in the soup object
        if tag.name in headers and tag.text != 'Contents':  # Check if the tag is a header tag and not the "Contents" tag
            # We try to find all paragraphs after it
            p = ''  # Initialize an empty string
            # loop through the next elements
            for ne in tag.next_elements:  # Loop through the next elements of the tag
                if ne.name == 'p':  # Check if the element is a p tag
                    p = p + get_paragraph_text(ne)  # Append the paragraph text of the element to the p string
                if ne.name in headers:  # Check if the element is a header tag
                    break  # Break the loop
            if p != '':  # Check if the p string is not empty
                section = [clean_wiki_content(tag.text), tag.name, clean_wiki_content(p)]  # Create a list of the section title, title tag, and paragraph text
                wiki_extract.append(section)  # Append the section list to the wiki extract list
    
    return wiki_extract  # Return the wiki extract list

def get_answers(question, url):
    # Function to get the answers from a given question and URL
    question_answerer = pipeline("question-answering", model='deepset/roberta-base-squad2')  # Create a question-answering pipeline using the deepset/roberta-base-squad2 model
    wiki_extract = get_wiki_extract(url)  # Get the wiki extract from the URL   
    answers = []  # Initialize an empty list
    for section in wiki_extract:  # Loop through the sections in the wiki extract
        result = question_answerer(question=question, context=section[2])  # Get the result from the question-answering pipeline using the question and the section paragraph as the context
        answer = {'title': section[0], 'title_tag': section[1], 'paragraph': section[2], **result }  # Create a dictionary of the section title, title tag, paragraph, and the result
        answers.append(answer)  # Append the answer dictionary to the answers list

    return answers  # Return the answers list

def get_html_answers(question, url, top_n=3):
    # Function to get the HTML answers from a given question, URL, and top_n
    answers = get_answers(question, url)  # Get the answers from the question and URL
    df = pd.DataFrame(answers)  # Convert the answers list to a data frame
    n_sections = len(df)  # Get the number of sections in the data frame
    if n_sections <= top_n:  # Check if the number of sections is less than or equal to the top_n
        df_answers = df.nlargest(n_sections, 'score')  # Get the data frame with the highest scores
    else:  # If the number of sections is greater than the top_n
        df_answers = df.nlargest(top_n, 'score')  # Get the data frame with the top_n highest scores

    html_answers = ""  # Initialize an empty string
    for index, row in df_answers.iterrows():  # Loop through the rows in the data frame
        title = row['title']  # Get the title
        title_tag = row['title_tag']  # Get the title tag
        paragraph = row['paragraph']  # Get the paragraph
        par_start = 0  # Set the paragraph start index to 0
        par_end = len(paragraph) - 1  # Set the paragraph end index to the length of the paragraph minus 1
        ans_start = row['start']  # Get the answer start index
        ans_end = row['end']  # Get the answer end index
        ans = row['answer']  # Get the answer
        score = round(row['score'] * 100, 2)  # Get the score and round it to two decimal places
        
        html_answer = f"""
        <p style="background-color: BlanchedAlmond">
            <span style="color: purple; font-weight: bold;">Answer: </span>
            <span>{ans}</span>
            <span style="color: purple; font-weight: bold;">Score: </span>
            <span>{score} %</span>
        </p>
        <{title_tag}>{title}</{title_tag}>
        <p>
            <span>{paragraph[par_start:ans_start-1]}</span>
            <span style="background-color: lightgreen;">{paragraph[ans_start:ans_end]}</span>
            <span>{paragraph[ans_end:par_end]}</span>
        </p>
        <br>
        """
        
        html_answers =  html_answers + html_answer  # Append the HTML answer to the HTML answers string

    return(html_answers)  # Return the HTML answers string
