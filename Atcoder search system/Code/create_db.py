import sqlite3
import requests
import re
from bs4 import BeautifulSoup

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

for a in range(5):
    url = 'https://atcoder.jp/contests/abc100/submissions?f.Task=abc100_b&f.LanguageName=&f.Status=AC&f.User=&page=' + str(a+1)
    html = requests.get(url)
    soup = BeautifulSoup(html.content, 'html.parser')

    num = 0
    m = 0

    for i in soup.find_all('tbody'):
            
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

db_name = 'atcoder.db'
con = sqlite3.connect(db_name)
cur = con.cursor()

def create_db():
    cur.execute('CREATE TABLE atcoder(id INTEGER, user STRING,\
    rating STRING, language STRING,code_len STRING,\
    runtime STRING, memory STRING, code STRING)')

    for i in range(100):
        sql = ('INSERT INTO atcoder (id, user, rating,\
            language, code_len, runtime, memory, code)\
            VALUES(?,?,?,?,?,?,?,?)')

        data = (i, user[i], rating[i], language[i],
                code_len[i], runtime[i], memory[i], code[i])

        cur.execute(sql, data)

try:
    create_db()

except sqlite3.OperationalError:
    cur.execute('DROP TABLE atcoder')
    create_db()

con.commit()

cur.close()
con.close()