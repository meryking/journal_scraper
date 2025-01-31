import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("🔍 Web Scraper App")

# User input for URL
url = st.text_input("Enter a website URL:")

if st.button("Scrape"):
    if url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            #find the text under div class ara-body
            text = soup.find('div', class_='ara-body')  
            # Extract all paragraphs within the main content
            if text:
                paragraphs = text.find_all("p")  # Find all <p> tags
                text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)  # Combine and clean text
                # print(article_content)

            if text:
                st.subheader("Scraped Text:")
                st.text_area("", text, height=300)
            else:
                st.warning("No text found!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")
