from ..common import common
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as sa


def set_secrets():
    # load environmental vars
    env_path = os.join(os.dirname(__file__), ".env")
    load_dotenv(env_path)

    common.db_name = os.environ.get("DB_NAME")


def set_db():
    engine = sa.create_engine(url="sqlite:///{common.db_name}", echo=True)
    common.session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
