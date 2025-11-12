import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse # Used for constructing absolute URLs and quoting parameters

from scrape import scrape_article

# Function to be called when a sidebar button is clicked
def set_article_url(url_to_set):
    # This updates the state of the main text input
    st.session_state.user_url_input = url_to_set
    # Note: st.experimental_rerun() is often not needed inside the callback
    # as the button click and state change naturally trigger a rerun.

# Function to print warning
def display_warning():
    """Display error and show current_url"""
    st.warning(
f"""**Oops! Something went wrong.**
Could it be that the article is not behind a paywall?\n
Try accessing it directly: [{current_url}]({current_url}).
""")


# --- 1. CONFIGURATION ---
st.title(f"[🔍 ARA.cat Web Scraper](https://arascraper.streamlit.app)")
st.markdown("---")

# Get article URL from query parameters (if set by sidebar link) or set a default empty string.
# This is how we read the URL after a sidebar link is clicked.
query_params = st.query_params
initial_url = query_params.get("article_url", [""])[0]

# User input for URL. The 'value' is pre-filled if a query parameter exists.
url = st.text_input("Enter a valid ARA article URL (or select from sidebar):", value=initial_url, key="user_url_input")

# --- 2. SIDEBAR HEADLINES FETCHING ---
st.sidebar.header("Today's Headlines:")
st.sidebar.caption("Click a headline to scrape its content.")

try:
    # Set headers to mimic a normal browser request
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    main_page = requests.get("https://www.ara.cat/", headers=HEADERS, timeout=10)
    main_page.raise_for_status()

    soup = BeautifulSoup(main_page.content, 'html.parser')
    results = []
    article_elements = soup.select('article.article, .combo-piece')

    for article in article_elements:

        headline_tag = article.find('h2')
        link_tag = article.find('a', href=True)

        if link_tag and headline_tag:
            title = headline_tag.get_text(strip=True)
            href = link_tag.get('href', 'No Link Found')
            
            # Construct the full absolute URL
            full_href = urllib.parse.urljoin("https://www.ara.cat/", href)
            
            # Use st.link_button to create a clickable element that changes the URL query parameter.
            # This triggers a full app rerun with the new 'article_url', which is then read in Step 1.
            st.sidebar.button(
                label=title,
                help=f"Click to scrape: {full_href}",
                #on_click=lambda: set_article_url(full_href),  # This function is called when the button is clicked
                on_click=set_article_url,  # This function is called when the button is clicked
                args=(href,)
            )

except requests.exceptions.RequestException as e:
    st.sidebar.error(f"Error fetching headlines: {e}")
except Exception as e:
    st.sidebar.error(f"An unexpected error occurred in sidebar: {e}")


# --- 3. MAIN SCRAPER LOGIC ---

# Automatically run scrape if a URL was passed via the sidebar link (initial_url is not empty)
# OR if the user manually clicks the 'Scrape' button.
run_scrape = (st.session_state.user_url_input != "") or (initial_url != "") or st.button("Scrape")

if run_scrape:
    # Use the current value from the text input
    current_url = st.session_state.user_url_input 
    
    if current_url:
        try:
            # Re-use headers from sidebar
            # page = requests.get(current_url, headers=HEADERS, timeout=15)
            # page.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            # soup = BeautifulSoup(page.content, 'html.parser')
            soup = scrape_article(current_url)
            
            # --- EXTRACT TITLE/SUBTITLE/BODY ---
            title_tag = soup.find('h1')
            subtitle_tag = soup.find('h2')
            text_div = soup.find('div', class_='ara-body')  
            # Get image
            original_source_tag = soup.select_one('picture img[src*=".jpg"]')
            # Some images are in png format, but only get them if no jpg exists
            # Enter if statement if original_source_tag is none
            if not original_source_tag:
                original_source_tag = soup.select_one('picture img[src*=".png"]')

            image_url = original_source_tag.get("src") if original_source_tag else None
            image_caption = original_source_tag.get("alt") if original_source_tag else None
            
            if text_div:
                # Remove specific spans (like 'place') that are often used for interactive or non-text content
                for span in text_div.find_all('span', class_='place'):
                    span.decompose()
                
                # Extract and join all paragraphs within the main content area
                paragraphs = text_div.find_all("p")
                article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
                
                # Display Header information
                if title_tag:
                    st.header(title_tag.text)
                
                if subtitle_tag:
                    st.subheader(subtitle_tag.text)
                if image_url:
                    st.image(image_url)#, caption=image_caption)  

                if article_content:
                    st.text(article_content)
                    st.markdown(f"**Source URL:** [{current_url}]({current_url})")
                    st.markdown("---")
                # Raise warning if there is no image nor article_content
                if not article_content and not image_url:
                    st.warning("Found main body tag, but no readable paragraphs were extracted.")
            else:
                display_warning()

        except requests.exceptions.HTTPError as errh:
            display_warning()
        except requests.exceptions.RequestException as erre:
            st.error(f"An error occurred during request: {erre}")
            display_warning()
        except Exception as e:
            st.error(f"An unexpected error occurred during scraping: {e}")
            display_warning()
    else:
        st.warning("Please enter a valid URL.")