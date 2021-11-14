import sqlite3  #SQLite
import requests  #HTMLにアクセス&データ取得
import re  #compile関数を用いる
from itertools import groupby  #配列のグループ分け
from bs4 import BeautifulSoup  #HTMLから特定のデータを抽出する
from flask import Flask, render_template, request  #Flask

app = Flask(__name__)

date = []
user = []
rating = []
language = []
code_len = []
runtime = []
memory = []
code = []

def get_code(code_url, num2):

    code_html = requests.get(code_url)
    code_soup = BeautifulSoup(code_html.content, 'html.parser')
    for k in code_soup.find_all('pre'):
        if num2 == 0:
            code.append(k.text)
        num2 += 1

def get_rating(user_url, num3, i):

    judge = False

    user_html = requests.get(user_url)
    user_soup = BeautifulSoup(user_html.content, 'html.parser')
    
    for k in user_soup.find_all('span', class_ = re.compile('user-')):
        if num3 == 1:
            rating.append(k.text)
            judge = True
        num3 += 1

    if judge == False:
        rating.append(0)

url = 'https://atcoder.jp/contests/abc100/submissions?f.Task=abc100_b&f.LanguageName=&f.Status=AC&f.User=&page='
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')

title = soup.find('a', class_ = 'contest-title')
problem = soup.find(href = re.compile('/abc100_b'))

for a in range(5):
        url = 'https://atcoder.jp/contests/abc100/submissions?f.Task=abc100_b&f.LanguageName=&f.Status=AC&f.User=&page=' + str(a+1)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')

        num = 0
        m = 0

        for i in soup.find_all('tbody'):

            for j in i.find_all('time', class_ = 'fixtime-second'):
                date.append(j.text)
                
            for j in i.find_all(href = re.compile('/users')):
                user.append(j.text)
                get_rating('https://atcoder.jp' + j.attrs['href'], 0, m)
                m += 1
                
            for j in i.find_all(href = re.compile('Language')):
                language.append(j.text)
                
            for j in i.find_all('td', class_ = 'text-right'):
                if num % 4 == 1:
                    code_len.append(j.text)
                elif num % 4 == 2:
                    runtime.append(j.text)
                elif num % 4 == 3:
                    memory.append(j.text)
                num += 1
                
            for j in i.find_all(href = re.compile('/contests/abc100/submissions/')):
                get_code('https://atcoder.jp' + j.attrs['href'], 0)

data_list = []
for i in range(100):
    data_list.append((date[i], user[i], rating[i], language[i], code_len[i], runtime[i], memory[i], code[i]))

data_list.sort(key = lambda x: x[3])

for i in range(100):
    date[i] = data_list[i][0]
    user[i] = data_list[i][1]
    rating[i] = data_list[i][2]
    language[i] = data_list[i][3]
    code_len[i] = data_list[i][4]
    runtime[i] = data_list[i][5]
    memory[i] = data_list[i][6]
    code[i] = data_list[i][7]

db_name = 'atcoder_list.db'
con = sqlite3.connect(db_name)
cur = con.cursor()

try:
    cur.execute('CREATE TABLE atcoder(id INTEGER, date STRING,\
    user STRING, rating STRING, language STRING,code_len STRING,\
    runtime STRING, memory STRING, code STRING)')

    for i in range(100):
        sql = ('INSERT INTO atcoder (id, date, user, rating,\
            language, code_len, runtime, memory, code)\
            VALUES(?,?,?,?,?,?,?,?,?)')

        data = (i, date[i], user[i], rating[i], language[i],
                code_len[i], runtime[i], memory[i], code[i])

        cur.execute(sql, data)
    
except sqlite3.OperationalError:
    None

con.commit()

cur.execute('SELECT * FROM atcoder')
db_data = cur.fetchall()

cur.close()
con.close()

@app.route('/')
def main():

    return render_template('first.html', title = title.text, second_title = problem.text)

@app.route('/Working')
def second():

    return render_template('second.html', title = title.text + ' Working', data = db_data)

if __name__ == '__main__':
    app.run(debug = True)