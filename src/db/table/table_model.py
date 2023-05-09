from sqlalchemy.ext.automap import automap_base
from sqlalchemy.engine.base import Engine


Base = automap_base()

Problem = Base.classes.problems  # problems TBL
User = Base.classes.users  # users TBL
Submission = Base.classes.submissions  # submissions TBL


def create_table(engine: Engine) -> None:
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
