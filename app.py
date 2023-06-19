import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import json

api_key = st.text_input("Enter your OpenAI API key", type="password")

if api_key:
    openai.api_key = api_key

    url = st.text_input("Enter the URL to scrape")

    if url:
        st.write(f"Scraping {url}...")

        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "html.parser")

        text = ' '.join([p.text for p in soup.find_all('p')])

        model_name = "gpt-4-0613"

        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant."},
                {"role": "user", "content": text},
            ],
        )

        st.write(response.choices[0].message['content'])
