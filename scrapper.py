import requests
from bs4 import BeautifulSoup

"""# TODO: 
que el programa sigui una pagina web
crear un espai per copiar la url de l'article
que l'output es vegi a la pagina web html amb el text de l'article
agfegir el titular i subtitol

"""

url="https://www.ara.cat/economia/immobiliari/sanchez-promet-mes-bonificacions-fiscals-als-propietaris-posin-pis-lloguer_1_5253414.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
#find the text under div class ara-body
text = soup.find('div', class_='ara-body')  
 # Extract all paragraphs within the main content
if text:
    paragraphs = text.find_all("p")  # Find all <p> tags
    article_content = "\n\n".join(p.get_text(strip=True) for p in paragraphs)  # Combine and clean text
    print(article_content)