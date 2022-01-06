from consts import PEOPLE_NUM
from consts import CONTEST_NUM
from create_data_db import set_db

import sqlite3
import requests
import re
from bs4 import BeautifulSoup
import collections
from flask import Flask, render_template, request

app = Flask(__name__)

def set_data():

    db_name = 'atcoder.db'
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    cur.execute('SELECT * FROM atcoder')

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

user = []
rating = []
language = []
code_len = []
runtime = []
memory = []
code = []

@app.route('/')
def start():

    return render_template('index.html', contest_num = CONTEST_NUM)

@app.route('/Working', methods=['GET', 'POST'])
def languages():

    if request.method == 'POST':
        CONTEST = request.form.get('contest')
        PROBLEM = request.form.get('problem')
    
    set_db(CONTEST, PROBLEM)

    set_data()

    c_language = collections.Counter(language)

    language_key = list(c_language.keys())
    language_value = list(c_language.values())

    return render_template('language.html', language_key = language_key, language_value = language_value, language_len = PEOPLE_NUM)

@app.route('/Working/Users', methods=['GET', 'POST'])
def users():

    if request.method == 'POST':
        your_lang = request.form['language']
    
    user_key = []
    user_value = []

    for i in range(PEOPLE_NUM):
        if language[i] == your_lang:
            user_key.append(user[i])
            user_value.append(rating[i])

    return render_template('user.html', user_key = user_key, user_value = user_value, user_len = len(user_key))

@app.route('/Working/Users/Details', methods=['GET', 'POST'])
def codes():

    if request.method == 'POST':
        your_user = request.form['user']
    
    for i in range(PEOPLE_NUM):
        if user[i] == your_user:
            code_len_key = code_len[i]
            runtime_key = runtime[i]
            memory_key = memory[i]
            code_key = code[i]

    return render_template('code.html', code_len_key = code_len_key, runtime_key = runtime_key, memory_key = memory_key, code_key = code_key)

if __name__ == '__main__':
    app.run(debug = True)