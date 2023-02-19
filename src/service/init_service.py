from ..common import common
from dotenv import load_dotenv
import os
from sqlalchemy.orm import sessionmaker, scoped_session
import sqlalchemy as sa


# load environmental vars
def set_secrets():
    env_path = os.join(os.dirname(__file__), ".env")
    load_dotenv(env_path)

    common.db_name = os.environ.get("DB_NAME")


# set db info
def set_db():
    engine = sa.create_engine(
        url="sqlite:///{common.db_name}", encoding="utf-8", echo=True
    )
    common.session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
