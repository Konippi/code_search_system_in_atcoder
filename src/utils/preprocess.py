def convert_diff(diff: str) -> str:
    """
    指定した難易度をWebスクレイピング用に変換

    Parameters
    ----------
    diff: str
        変換前の難易度
    ----------

    Returns
    -------
    converted_diff: str
        変換後の難易度
    -------
    """
    return chr(ord(diff) - 2)


def combine_contest_with_diff(contest_num: int, diff: str) -> str:
    """
    Webスクレイピング用にコンテストと難易度を結合

    Parameters
    ----------
    contest_num: int
        コンテスト番号
    diff: str
        難易度
    ----------

    Returns
    -------
    combined_contest_with_diff: str
        Webスクレイピング用に結合されたコンテストと難易度
    -------
    """
    converted_contest = ""
    if 42 <= contest_num <= 50:
        converted_contest = str(contest_num + 16)
    elif 52 <= contest_num <= 53:
        converted_contest = str(contest_num + 15)
    elif 55 <= contest_num <= 56:
        converted_contest = str(contest_num + 14)
    elif 58 <= contest_num <= 60:
        converted_contest = str(contest_num + 13)
    elif 62 <= contest_num <= 63:
        converted_contest = str(contest_num + 12)
    elif 65 <= contest_num <= 69:
        converted_contest = str(contest_num + 11)
    elif 71 <= contest_num <= 72:
        converted_contest = str(contest_num + 10)
    elif contest_num == 74:
        converted_contest = str(contest_num + 9)
    elif 77 <= contest_num <= 78:
        converted_contest = str(contest_num + 7)
    elif 81 <= contest_num <= 83:
        converted_contest = str(contest_num + 5)
    elif 86 <= contest_num <= 87:
        converted_contest = str(contest_num + 3)
    elif 90 <= contest_num <= 95:
        converted_contest = str(contest_num + 1)
    elif 97 <= contest_num <= 98:
        converted_contest = str(contest_num)
    elif 101 <= contest_num <= 102:
        converted_contest = str(contest_num - 2)
    elif 107 <= contest_num <= 108:
        converted_contest = str(contest_num - 6)
    else:
        converted_contest = str(contest_num - 8)

    combined_contest_with_diff = f"arc{converted_contest.zfill(3)}_{convert_diff(diff)}"

    return combined_contest_with_diff
