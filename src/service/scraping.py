from common import common
from utils import preprocess
from main import app
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
import re
import time


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

    target = soup.find(href=re.compile(r"/contests/abc")).get("href")
    latest_contest = re.search(r"abc(.*)", target).group()
    latest_contest_num = int(latest_contest.replace("abc", ""))

    return latest_contest_num


def get_pair_diffs(contest_num: int) -> dict[str, str]:
    """
    指定したコンテストにおける問題の難易度一覧を取得

    Parameters
    ----------
    contest_num: int
        コンテスト番号
    ----------

    Returns
    -------
    pair_diff_dict: dict[str, str]
        (難易度一覧: Webスクレイピング用の難易度一覧)
    -------
    """
    if contest_num < 20:
        return {"A": "1", "B": "2", "C": "3", "D": "4"}
    elif contest_num <= 125:
        return {"A": "a", "B": "b", "C": "c", "D": "d"}
    elif contest_num <= 211:
        return {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f"}
    else:
        return {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "G": "g", "Ex": "h"}


def get_target_submission_info(latest_contest_num: int) -> dict[list[str, int | str]]:
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
    target_submission_info_list = []

    for contest_num in range(1, latest_contest_num + 1):
        pair_diff_dict = get_pair_diffs(contest_num=contest_num)
        str_contest = str(contest_num).zfill(3)
        for diff, diff_for_scraping in pair_diff_dict.items():
            if 42 <= contest_num <= 111 and diff_for_scraping in ["c", "d"]:
                combined_contest_with_diff = preprocess.combine_contest_with_diff(
                    contest_num=contest_num, diff=diff_for_scraping
                )
            else:
                combined_contest_with_diff = f"abc{str_contest}_{diff_for_scraping}"

            submissions_url = (
                f"https://atcoder.jp/contests/abc{str_contest}/"
                f"submissions?f.Task={combined_contest_with_diff}&f.Status=AC"
            )
            target_submission_info_list.append({"contest": contest_num, "diff": diff, "url": submissions_url})

    return target_submission_info_list


def get_rating(url: str) -> int:
    """
    レートを取得

    Parameters
    ----------
    url: str
        レート取得先のURL
    ----------

    Returns
    -------
    rating: int
        レート
    -------
    """
    html = requests.get(url=url, headers={"User-Agent": common.UA})
    soup = BeautifulSoup(html.content, "html.parser")

    # レートなしユーザの判定
    if len(soup.find_all("canvas")) == 0:
        return 0

    rating = int(soup.find_all("span", class_=re.compile(r"user-"))[2].text)

    return rating


def get_code(url: str) -> str:
    """
    ソースコードを取得

    Parameters
    ----------
    url: str
        ソースコード取得先のURL
    ----------

    Returns
    -------
    code: str
        ソースコード
    -------
    """
    html = requests.get(url=url, headers={"User-Agent": common.UA})
    soup = BeautifulSoup(html.content, "html.parser")
    code = soup.find("pre", id="submission-code").text

    return code


def get_submissions(target_submission_info: dict[str, str | int]) -> dict[str, int | str | list]:
    """
    提出情報を取得

    Parameters
    ----------
    target_submission_info: dict[str, str | int]
        提出情報のスクレイピング対象情報
    ----------

    Returns
    -------
    submission_dto_list: dict[str, int | str | list]
        提出情報
    -------
    """
    url = target_submission_info["url"]
    contest_num = target_submission_info["contest"]
    diff = target_submission_info["diff"]
    html = requests.get(url=url, headers={"User-Agent": common.UA})
    soup = BeautifulSoup(html.content, "html.parser")

    # title
    title = re.sub(r"(.+)\s-\s", "", soup.find(href=re.compile(r"/contests/abc\d{3}/tasks/")).text)

    # user name and rating
    user_name_with_rating_list = [
        (user.text, get_rating(url=f"https://atcoder.jp{user.attrs['href']}"))
        for user in soup.find_all(href=re.compile(r"/users"))
    ]

    # language
    language_list = [language.text for language in soup.find_all(href=re.compile(r"Language"))]

    # code length
    code_len_list = [
        code_len.text for idx, code_len in enumerate(soup.find_all("td", class_="text-right")) if (idx - 1) % 4 == 0
    ]

    # source code
    code_list = [
        get_code(url=f"https://atcoder.jp{code.attrs['href']}")
        for code in soup.find_all(href=re.compile(r"/contests/abc\d{3}/submissions/(.+)"))
    ]

    return {
        "contest": contest_num,
        "diff": diff,
        "title": title,
        "users": user_name_with_rating_list,
        "languages": language_list,
        "code_lens": code_len_list,
        "codes": code_list,
    }


def get_submission_dto() -> dict[str, int | str | list]:
    """
    提出情報dtoを取得

    Returns
    -------
    submission_dto_list: dict[str, int | str | list]
        提出情報dto
    -------
    """
    latest_contest_num = get_latest_contest_num()
    target_submission_info_list = get_target_submission_info(latest_contest_num=latest_contest_num)

    # parallel process
    with ThreadPoolExecutor(max_workers=4) as executor:
        submission_dto_list = list(executor.map(get_submissions, target_submission_info_list))

    app.logger.info(submission_dto_list)

    return submission_dto_list
