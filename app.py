import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("🔍 Web Scraper App")

# User input for URL
url = st.text_input("Enter a website URL:")
#url = "https://www.ara.cat/economia/mercats/xina-respon-als-aranzels-trump-taxes-d-10-15_1_5274974.html"

if st.button("Scrape"):
    if url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find('h1')
            subtitle = soup.find('h2')
            # soup.find('div', class_='subtitle')
    
            #find the text under div class ara-body
            text = soup.find('div', class_='ara-body')  
            if title:
                st.title(title.text)
            
            else:
                st.warning("No title found!")

            if subtitle:
                st.header(subtitle.text)        
            else:
                st.warning("No subtitle found!")

            # Extract all paragraphs within the main content
            if text:
                paragraphs = text.find_all("p")  # Find all <p> tags
                text = "\n\n".join(p.get_text(strip=True) for p in paragraphs)  # Combine and clean text
                # print(article_content)
                st.text(text)
            else:
                st.warning("No text found!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid URL.")
