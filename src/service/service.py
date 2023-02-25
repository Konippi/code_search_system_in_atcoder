from common import common
from repository import repository
from . import scraping
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as sa
import requests
import re
import os


def set_secrets() -> None:
    """
    環境変数を読込
    """
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)
    common.DB_NAME = os.environ.get("DB_NAME")
    common.UA = os.environ.get("UA")


def set_db_session() -> None:
    """
    dbセッションを確立
    """
    engine = sa.create_engine(url=f"sqlite:///{common.DB_NAME}.db", encoding="utf-8", echo=True)
    common.SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def set_atcoder_data():
    submissions_info_list = scraping.get_submissions_info()
