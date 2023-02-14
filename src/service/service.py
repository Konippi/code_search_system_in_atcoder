from ..common import common
from dotenv import load_dotenv
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
import os


def set_secrets():
    # load environment vars
    env_path = os.join(os.dirname(__file__), ".env")
    load_dotenv(env_path)

    common.db_name = os.environ.get("DB_NAME")


def set_db():
    engine = sa.create_engine(url="sqlite:///{common.db_name}")
    common.session = sessionmaker(bind=engine)
