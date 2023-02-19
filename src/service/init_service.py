from ..common import common
from ..repository import scraping_repository
from . import scraping_service
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as sa
import os


# load environmental vars
def set_secrets():
    env_path = os.join(os.dirname(__file__), ".env")
    load_dotenv(env_path)

    common.db_name = os.environ.get("DB_NAME")
    common.UA = os.environ.get("UA")


# set db session
def set_db_session():
    engine = sa.create_engine(
        url="sqlite:///{common.db_name}.db", encoding="utf-8", echo=True
    )
    common.session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )


def set_atcoder_data():
    user_list = scraping_service.get_users()
    problem_list = scraping_service.get_problems()
    submission_list = scraping_service.get_submissions()
