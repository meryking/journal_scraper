"""
Module to scrape content from newspaper
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

# SIDEBAR PART:



# NEWSPAPER URL PART:

def scrape_article(url):
    """
    Scrape content from a given URL.

    Args:
        url (str): The URL of the newspaper article.

    Returns:
        soup: The scraped content of the article.
    """
    page = requests.get(url, headers=HEADERS, timeout=15)
    page.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def extract_image_tag(soup):
    """
    # TODO: Should it go to processing module?
    Extracts the image tag from the soup object. Tries .jpg, if not .png.

    Args:
        soup (BeautifulSoup): The soup object containing the article content.

    Returns:
        image_tag: The image tag, None if not found.
    """
    # Get image
    image_tag = soup.select_one('picture img[src*=".jpg"]')
    # Some images are in png format, but only get them if no jpg exists
    # Enter if statement if original_source_tag is none
    if not image_tag:
        image_tag = soup.select_one('picture img[src*=".png"]')
    
    return image_tag

def extract_params_from_soup(soup):
    """
    Extracts parameters from the soup object.

    Args:
        soup (BeautifulSoup): The soup object containing the article content.

    Returns:
        tuple: A tuple containing the extracted parameters.
    """
    title_tag = soup.find('h1')
    subtitle_tag = soup.find('h2')
    text_div = soup.find('div', class_='ara-body')  
    image_tag = extract_image_tag(soup)
    return title_tag, subtitle_tag, text_div, image_tag


