from common import common
from repository import repository
from . import scraping
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as sa
import requests
import re
import os


# load environmental vars
def set_secrets() -> None:
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)
    common.db_name = os.environ.get("DB_NAME")
    common.UA = os.environ.get("UA")


# set db session
def set_db_session() -> None:
    engine = sa.create_engine(
        url=f"sqlite:///{common.db_name}.db", encoding="utf-8", echo=True
    )
    common.session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


def set_atcoder_data():
    problem_list = scraping.get_problems()
    # user_list = scraping.get_users()
    # submission_list = scraping.get_submissions()
