# https://news.naver.com/
# 검찰

import requests
from bs4 import BeautifulSoup
import pandas


def getArticleContents(url, body):
    raw = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    html = BeautifulSoup(raw.text, "html.parser")
    print(url, body)
    articles = html.select_one(body).text
    # title = ar.select_one("a.news_tit").text

    return articles.strip()


base_url = "https://search.naver.com/search.naver?where=news"

keyword = "query=" + input("검색할 뉴스의 키워드: ")

sort = "sort={0}".format(input("정렬, 0: 연관도, 1: 최신순, 2: 오래된순"))
date_range = "pd={0}".format(3)
from_date = "ds={0}".format(input("시작날짜(ex. 2021.03.21)"))

to_date = "de={0}".format(input("끝 날짜(ex. 2021.03.21)"))

page_num = 0
page = "start={0}".format(1)
url = "&".join([base_url, keyword, sort, date_range, from_date, to_date, page])
raw = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
)
html = BeautifulSoup(raw.text, "html.parser")
articles = html.select("ul.list_news > li")


article_list = []
while articles != []:
    for ar in articles:
        content = None
        title = ar.select_one("a.news_tit").text
        source = ar.select_one("a.info").text
        link = ar.select_one("a.news_tit").attrs["href"]
        date = ar.select_one("span.info").text

        if source == "연합뉴스":
            body = "article.story-news.article"
            content = getArticleContents(link, body)
            article_list.append([title, source, link, date, content])
        # elif source == "조선일보":
        #     body = "~~~"
        #     content = getArticleContents(link, body)
        #     article_list.append([title, source, link, date, content])
        else:
            article_list.append([title, source, link, date, None])

    page_num += 1
    page = "start={0}".format(1 + (page_num * 10))
    url = "&".join([base_url, keyword, sort, date_range, from_date, to_date, page])
    raw = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    html = BeautifulSoup(raw.text, "html.parser")
    articles = html.select("ul.list_news > li")

df = pandas.DataFrame(
    article_list, columns=["Title", "Source", "link", "date", "content"]
)

df.to_csv(
    "./test.csv",
    sep=",",
)  # do not write index
