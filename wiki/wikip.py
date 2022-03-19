import requests
from bs4 import BeautifulSoup
import random
import wikipedia

def wikiRandom():
    lst = ['Data', 'Algorithms', 'Data analysis', 'Cloud computing', 'Python (programming language) development tools']
    cate = random.choice(lst)
    print(f'The Category is {cate}')
    url = requests.get(f"https://en.wikipedia.org/wiki/Special:RandomInCategory/{cate}")
    soup = BeautifulSoup(url.content, "html.parser")
    title = soup.find(class_="firstHeading").text
    print(f"{title}")
    cnt = wikipedia.page(title).content
    return cnt