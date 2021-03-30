import requests
from bs4 import BeautifulSoup
import pandas

raw = requests.get(
    "https://www.yna.co.kr/view/AKR20210322134700005?input=1195m",
    headers={"User-Agent": "Mozilla/5.0"},
)
html = BeautifulSoup(raw.text, "html.parser")
articles = html.select_one("article.story-news.article").text
# title = ar.select_one("a.news_tit").text

print(articles.strip())