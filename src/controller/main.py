from flask import Flask, render_template, request
from sqlalchemy.orm import sessionmaker
from ..service import service
import sqlite3
import requests
import re
from bs4 import BeautifulSoup
import collections


app = Flask(
    __name__, static_folder="frontend/static", template_folder="frontend/templates"
)

user = []
rating = []
language = []
code_len = []
runtime = []
memory = []
code = []
your_lang = ""


@app.before_first_request
def init():
    service.set_secrets()


def initialization():
    user.clear()
    rating.clear()
    language.clear()
    code_len.clear()
    runtime.clear()
    memory.clear()
    code.clear()


def set_data(CONTEST, PROBLEM):

    db_name = "atcoder.db"
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute("SELECT * FROM atcoder_" + CONTEST + "_" + PROBLEM)

    for data in cur:
        user.append(data[1])
        rating.append(data[2])
        language.append(data[3])
        code_len.append(data[4])
        runtime.append(data[5])
        memory.append(data[6])
        code.append(data[7])

    cur.close()
    con.close()


@app.route("/", methods=["GET"])
def init():
    service.set_env_var()
    service.set_db()
    return render_template("index.html", contest_num=CONTEST_NUM)


@app.route("/Working", methods=["GET", "POST"])
def languages():

    if request.method == "POST":
        CONTEST = request.form.get("contest")
        PROBLEM = request.form.get("problem")
        initialization()

    set_data(CONTEST, PROBLEM)

    c_language = collections.Counter(language)

    language_key = list(c_language.keys())
    language_value = list(c_language.values())

    return render_template(
        "language.html",
        language_key=language_key,
        language_value=language_value,
        language_len=PEOPLE_NUM,
    )


@app.route("/Working/Users", methods=["GET", "POST"])
def users():

    global your_lang

    if request.method == "POST":
        your_lang = request.form["language"]
        code_search_judge = request.form["range"]  # 0:ソースコード検索なし, 1:ソースコード検索あり

    user_key = []
    user_value = []

    for i in range(PEOPLE_NUM):
        if language[i] == your_lang:
            user_key.append(user[i])
            user_value.append(rating[i])

    if code_search_judge == "1":
        return render_template("code_search.html")

    return render_template(
        "user.html", user_key=user_key, user_value=user_value, user_len=len(user_key)
    )


@app.route("/Working/Users/Details", methods=["GET", "POST"])
def codes():

    if request.method == "POST":
        your_user = request.form["user"]

    for i in range(PEOPLE_NUM):
        if user[i] == your_user:
            code_len_key = code_len[i]
            runtime_key = runtime[i]
            memory_key = memory[i]
            code_key = code[i]

    return render_template(
        "code.html",
        code_len_key=code_len_key,
        runtime_key=runtime_key,
        memory_key=memory_key,
        code_key=code_key,
    )


@app.route("/Working/Search_Code", methods=["GET", "POST"])
def serach_code():

    if request.method == "POST":
        your_code = request.form["your_code"]

    levenshtein = []

    for i in range(PEOPLE_NUM):
        if language[i] == your_lang:
            levenshtein.append(lev.ratio(your_code, code[i]))

    ans = levenshtein.index(min(levenshtein))

    return render_template(
        "code.html",
        code_len_key=code_len[ans],
        runtime_key=runtime[ans],
        memory_key=memory[ans],
        code_key=code[ans],
    )


if __name__ == "__main__":
    app.run(debug=True)