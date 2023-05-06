from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.engine.base import Engine


Base = declarative_base()


# problemTBL
class Problem(Base):
    __tablename__ = "problem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest = Column(Integer, nullable=False)
    diff = Column(String(2), nullable=False)
    title = Column(String(64), nullable=False, unique=True)
    submission = relationship("Submission")


# userTBL
class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)
    submission = relationship("Submission")


# submissionTBL
class Submission(Base):
    __tablename__ = "submission"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    problem_id = Column(Integer, ForeignKey("problem.id", onupdate="CASCADE", ondelete="CASCADE"))
    language = Column(String(32), nullable=False)
    code_len = Column(String(8), nullable=False)
    code = Column(Text(), nullable=False)


def create_table(engine: Engine):
    """
    テーブルを作成

    Parameters
    ----------
    engine:
        DBエンジン
    ----------

    Returns
    -------
    None
    -------
    """
    Base.metadata.create_all(engine)
