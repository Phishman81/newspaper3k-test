import streamlit as st
from newspaper import Article

def scrape_url(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

st.title('URL Content Scraper')

url = st.text_input('Enter a URL', '')

if url:
    st.write('Scraping...')

    try:
        text = scrape_url(url)
        st.write(text)
    except Exception as e:
        st.write(f'Error: {e}')
