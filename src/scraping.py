from ..common import common
from bs4 import BeautifulSoup
import requests
import re


def get_latest_contest_num() -> int:
    url = "https://atcoder.jp/contests/archive?ratedType=1&category=0"
    html = requests.get(url=url, headers=common.UA)
    soup = BeautifulSoup(html.content, "html.parser")

    target = soup.find(href=re.compile("/contests/abc")).get("href")
    latest_contest_num = int(re.search(r"abc(.*)", target))
    return latest_contest_num


def get_problems():
    latest_contest_num = get_latest_contest_num()
    print(latest_contest_num)
