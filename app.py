import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse # Used for constructing absolute URLs and quoting parameters

# Function to be called when a sidebar button is clicked
def set_article_url(url_to_set):
    # This updates the state of the main text input
    st.session_state.user_url_input = url_to_set
    # Note: st.experimental_rerun() is often not needed inside the callback
    # as the button click and state change naturally trigger a rerun.

# --- 1. CONFIGURATION ---
st.title("🔍 ARA Web Scraper")
st.markdown("---")

# Get article URL from query parameters (if set by sidebar link) or set a default empty string.
# This is how we read the URL after a sidebar link is clicked.
query_params = st.query_params
initial_url = query_params.get("article_url", [""])[0]

# User input for URL. The 'value' is pre-filled if a query parameter exists.
url = st.text_input("Enter a valid ARA article URL:", value=initial_url, key="user_url_input")

# --- 2. SIDEBAR HEADLINES FETCHING ---
st.sidebar.header("Titulars del dia (ARA):")
st.sidebar.caption("Click a headline to scrape its content.")

try:
    # Set headers to mimic a normal browser request
    HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    main_page = requests.get("https://www.ara.cat/", headers=HEADERS, timeout=10)
    main_page.raise_for_status()
    main_soup = BeautifulSoup(main_page.content, 'html.parser')

    divs = main_soup.find_all('div', class_='combo-piece')

    count = 0
    for div in divs:
        link = div.find('a')  # Find the <a> inside the div
        if link and link.get('href') and link.get('title'):
            href = link.get('href')
            title = link.get('title')

            # Construct the full absolute URL
            
            full_href = urllib.parse.urljoin("https://www.ara.cat/", href)
            
            
            # Use st.link_button to create a clickable element that changes the URL query parameter.
            # This triggers a full app rerun with the new 'article_url', which is then read in Step 1.
            st.sidebar.button(
                label=title,
                key=f"btn_{count}",
                help=f"Click to scrape: {full_href}",
                #on_click=lambda: set_article_url(full_href),  # This function is called when the button is clicked
                on_click=set_article_url,  # This function is called when the button is clicked
                args=(href,)
            )

            
            
            count += 1
            if count >= 10: # Limit to 10 headlines
                break

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
            page = requests.get(current_url, headers=HEADERS, timeout=15)
            page.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            
            soup = BeautifulSoup(page.content, 'html.parser')
            
            # --- EXTRACT TITLE/SUBTITLE/BODY ---
            title_tag = soup.find('h1')
            subtitle_tag = soup.find('h2')
            text_div = soup.find('div', class_='ara-body')  

            if text_div:
                # Remove specific spans (like 'place') that are often used for interactive or non-text content
                for span in text_div.find_all('span', class_='place'):
                    span.decompose()

                # Display Header information
                if title_tag:
                    st.header(title_tag.text)
                
                if subtitle_tag:
                    st.subheader(subtitle_tag.text)
                
                st.markdown(f"**Source URL:** [{current_url}]({current_url})")
                st.markdown("---")

                # Extract and join all paragraphs within the main content area
                paragraphs = text_div.find_all("p")
                article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)
                
                if article_content:
                    st.text(article_content)
                else:
                    st.warning("Found main body tag, but no readable paragraphs were extracted.")
            else:
                st.warning("Could not find the main article body (`div class='ara-body'`). This page structure may have changed or the URL is not a standard ARA article.")

        except requests.exceptions.HTTPError as errh:
            st.error(f"HTTP Error: Could not reach the article or the URL is invalid. {errh}")
        except requests.exceptions.RequestException as erre:
            st.error(f"An error occurred during request: {erre}")
        except Exception as e:
            st.error(f"An unexpected error occurred during scraping: {e}")
    else:
        st.warning("Please enter a valid URL.")