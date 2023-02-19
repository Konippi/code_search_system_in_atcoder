from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# base class
Base = declarative_base()


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contest = Column(Integer, nullable=False)
    diff = Column(String(2), nullable=False)
    title = Column(String(128), nullable=False)
