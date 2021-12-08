import sqlite3
import requests
import re
from bs4 import BeautifulSoup
import collections
from flask import Flask, render_template, request

app = Flask(__name__)

url = 'https://atcoder.jp/contests/abc100/submissions?f.Task=abc100_b&f.LanguageName=&f.Status=AC&f.User=&page='
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')

title = soup.find('a', class_ = 'contest-title')
problem = soup.find(href = re.compile('/abc100_b'))

user = []
rating = []
language = []
code_len = []
runtime = []
memory = []
code = []

db_name = 'atcoder_list.db'
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

c_language = collections.Counter(language)

language_key = list(c_language.keys())
language_value = list(c_language.values())

@app.route('/')
def main():

    return render_template('first.html', title = title.text, second_title = problem.text)

@app.route('/Working')
def second():

    return render_template('second.html', title = problem.text, language_key = language_key, language_value = language_value, language_len = 100)

@app.route('/Working/Users', methods=['GET', 'POST'])
def third():

    if request.method == 'POST':
        your_lang = request.form['language']
    
    user_key = []
    user_value = []

    for i in range(100):
        if(language[i] == your_lang):
            user_key.append(user[i])
            user_value.append(rating[i])

    return render_template('third.html', title = problem.text, user_key = user_key, user_value = user_value, user_len = len(user_key))


@app.route('/Working/Users/Details', methods=['GET', 'POST'])
def final():

    if request.method == 'POST':
        your_user = request.form['user']
    
    for i in range(100):
        if(user[i] == your_user):
            code_len_key = code_len[i]
            runtime_key = runtime[i]
            memory_key = memory[i]
            code_key = code[i]

    return render_template('fourth.html', title = problem.text, code_len_key = code_len_key, runtime_key = runtime_key, memory_key = memory_key, code_key = code_key)

if __name__ == '__main__':
    app.run(debug = True)