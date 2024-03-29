from dotenv import load_dotenv
from typing import Optional, Tuple
from repository import repository
from handler.error.error_handler import InvalidEnvironmentVariable
from . import scraping
import os
import schedule
import time


def get_secrets() -> Tuple[str, str]:
    """
    環境変数を読込

    Parameters
    ----------
    None
    ----------

    Returns
    -------
    None
    -------
    """
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)
    db_name: Optional[str] = os.environ.get("DB_NAME")
    ua: Optional[str] = os.environ.get("UA")

    if db_name is None or ua is None:
        raise InvalidEnvironmentVariable()

    return db_name, ua


def set_atcoder_submissions(ua: str) -> None:
    """
    AtCoderの提出履歴を取得

    Parameters
    ----------
    ua: str
        ユーザーエージェント
    ----------

    Returns
    -------
    None
    -------
    """
    submission_dto_list = scraping.get_submission_dto()
    problem_record_list = []
    user_record_list = []
    submission_record_list = []
    for submission_dto in submission_dto_list:
        problem_record_list.append(
            {
                "contest": submission_dto["contest"],
                "diff": submission_dto["diff"],
                "title": submission_dto["title"],
            }
        )
        for submission_idx in range(len(submission_dto["users"])):
            user_name = submission_dto["users"][submission_idx][0]
            user_rating = submission_dto["users"][submission_idx][1]
            language = submission_dto["languages"][submission_idx]
            code_len = submission_dto["code_lens"][submission_idx]
            user_record_list.append(
                {
                    "name": user_name,
                    "rating": user_rating,
                }
            )
            submission_record_list.append(
                {
                    "user_id": repository.get_user_id_by_name(user_name),
                    "problem_id": repository.get_problem_id_by_contest_and_diff(
                        submission_dto["contest"], submission_dto["diff"]
                    ),
                    "language": language,
                    "code_len": code_len,
                }
            )


def update_atcoder_data() -> None:
    """
    提出履歴を更新(cron: Sat.23:00:00)

    Parameters
    ----------
    None
    ----------

    Returns
    -------
    None
    -------
    """
    schedule.every().saturday.at("23:00").do(set_atcoder_data)

    while True:
        schedule.run_pending()
        time.sleep(1)
