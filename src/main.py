from service import service
from flask import Flask, render_template

app = Flask(
    __name__,
    static_folder="../frontend/static",
    template_folder="../frontend/templates",
)


@app.before_first_request
def init() -> None:
    service.set_secrets()
    service.set_db_session()
    service.set_atcoder_data()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", contest_num=250)


if __name__ == "__main__":
    app.run(debug=True)
