from sqlalchemy.orm import sessionmaker, scoped_session
from common import const
from db.table import table_model
import sqlalchemy as sa


def set_db_session() -> None:
    """
    dbセッションを確立

    Parameters
    ----------
    None
    ----------

    Returns
    -------
    None
    -------
    """
    engine = sa.create_engine(url=f"sqlite:///{const.DB_NAME}.db", encoding="utf-8", echo=True)
    const.SESSION = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    table_model.create_table(engine)
