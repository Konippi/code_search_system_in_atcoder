from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine
from typing import Optional
from db.table import table_model
import sqlalchemy as sa


class Db:
    session: Optional[Session] = None

    def set_db_session(self, db_name: str) -> None:
        """
        dbセッションを確立

        Parameters
        ----------
        db_name: str
            データベース名
        ----------

        Returns
        -------
        None
        -------
        """
        engine: Engine = sa.create_engine(url=f"sqlite:///{db_name}.db", encoding="utf-8", echo=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
        table_model.create_table(engine)
