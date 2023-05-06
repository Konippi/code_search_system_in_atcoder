import logging


def set_log_config() -> None:
    """
    ログを設定

    Parameters
    ----------
    None
    ----------

    Returns
    -------
    None
    -------
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(filename="../logs/app.log", encoding="utf-8", mode="w"))
    logger.propagate = False
