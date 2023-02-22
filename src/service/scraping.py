from common import common
from utils import preprocess
from main import app
from bs4 import BeautifulSoup
import requests
import re


def get_latest_contest_num() -> int:
    """
    開催された最新ABCのコンテスト番号を取得

    Returns
    -------
    latest_contest_num: int
        最新のコンテスト番号
    -------
    """
    url = "https://atcoder.jp/contests/archive?ratedType=1&category=0"
    html = requests.get(url=url, headers={"User-Agent": common.UA})
    soup = BeautifulSoup(html.content, "html.parser")

    target = soup.find(href=re.compile("/contests/abc")).get("href")
    latest_contest = re.search(r"abc(.*)", target).group()
    latest_contest_num = int(latest_contest.replace("abc", ""))

    return latest_contest_num


def get_diffs(contest_num: int) -> list[str]:
    """
    指定したコンテストにおける問題の難易度一覧を取得

    Parameters
    ----------
    contest_num: int
        コンテスト番号
    ----------

    Returns
    -------
    diff_list: str
        難易度一覧
    -------
    """
    if contest_num < 20:
        return ["1", "2", "3", "4"]
    elif contest_num <= 125:
        return ["a", "b", "c", "d"]
    elif contest_num <= 211:
        return ["a", "b", "c", "d", "e", "f"]
    else:
        return ["a", "b", "c", "d", "e", "f", "g", "h"]


def get_target_submissions_urls(latest_contest_num: int) -> str:
    """
    Webスクレイピング対象のURL一覧を取得

    Parameters
    ----------
    latest_contest_num: int
        最新のコンテスト番号
    ----------

    Returns
    -------
    target_submissions_url_list: str
        Webスクレイピング対象のURL一覧
    -------
    """
    target_submissions_url_list = []
    for contest_num in range(1, latest_contest_num + 1):
        diff_list = get_diffs(contest_num=contest_num)
        str_contest = str(contest_num).zfill(3)
        for diff in diff_list:
            if 42 <= contest_num <= 111 and diff in ["c", "d"]:
                combined_contest_with_diff = preprocess.combine_contest_with_diff(
                    contest_num=contest_num, diff=diff
                )
            else:
                combined_contest_with_diff = f"abc{str_contest}_{diff}"
            submissions_url = f"https://atcoder.jp/contests/abc{str_contest}/submissions?f.Task={combined_contest_with_diff}&f.Status=AC"
            target_submissions_url_list.append(submissions_url)

    return target_submissions_url_list


def get_submissions():
    latest_contest_num = get_latest_contest_num()
    target_submissions_url_list = get_target_submissions_urls(
        latest_contest_num=latest_contest_num
    )
    app.logger.info(target_submissions_url_list)
