import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import json

openai.api_key = 'your-openai-api-key'

def scrape_website(url):
    # Send a request to the website
    r = requests.get(url)

    # Get the content of the request
    web_content = r.text

    # Create a BeautifulSoup object and specify the parser
    soup = BeautifulSoup(web_content, 'html.parser')

    # This is a simple extraction of all text within paragraph tags
    # Depending on the website structure, you might need to adjust this
    text = ' '.join([p.text for p in soup.find_all('p')])

    return text

st.title('Web Scraper App')

# User input for the URL
url = st.text_input('Enter a URL')

if url:
    # Define the function
    functions = [
        {
            "name": "scrape_website",
            "description": "Scrape the content of a website",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the website"
                    }
                },
                "required": ["url"]
            }
        }
    ]

    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Scrape the content of this website: {url}"}
        ],
        functions=functions
    )

    # Extract the function call from the response
    function_call = json.loads(response['choices'][0]['message']['function_call']['arguments'])

    # Check if the function name matches and if the argument matches the provided URL
    if function_call['name'] == 'scrape_website' and function_call['arguments']['url'] == url:
        # Perform the actual web scraping
        scraped_content = scrape_website(url)

        st.subheader('Scraped Content:')
        st.write(scraped_content)
