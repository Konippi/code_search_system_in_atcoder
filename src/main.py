from service import service
from flask import Flask, render_template
import logging
import os

app = Flask(
    __name__,
    static_folder="../frontend/static",
    template_folder="../frontend/templates",
)


def set_log_config() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(filename="../logs/app.log", encoding="utf-8", mode="w"))
    logger.propagate = False


@app.before_first_request
def init() -> None:
    service.set_secrets()
    service.set_db_session()
    service.set_atcoder_data()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", contest_num=250)


if __name__ == "__main__":
    set_log_config()
    app.run(debug=True)
