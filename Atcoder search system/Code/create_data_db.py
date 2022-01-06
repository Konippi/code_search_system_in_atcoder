from consts import PEOPLE_NUM

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

def get_code(code_url, count):

    code_html = requests.get(code_url)
    code_soup = BeautifulSoup(code_html.content, 'html.parser')
    for k in code_soup.find_all('pre'):
        if count == 0:
            code.append(k.text)
        count += 1

def get_rating(user_url, count):

    judge = False

    user_html = requests.get(user_url)
    user_soup = BeautifulSoup(user_html.content, 'html.parser')
    
    for k in user_soup.find_all('span', class_ = re.compile('user-')):
        if count == 1:
            rating.append(k.text)
            judge = True
        count += 1

    if judge == False:
        rating.append(0)

def create_db(cur):
    cur.execute('CREATE TABLE atcoder(id INTEGER, user STRING,\
    rating STRING, language STRING,code_len STRING,\
    runtime STRING, memory STRING, code STRING)')

    for i in range(PEOPLE_NUM):
        sql = ('INSERT INTO atcoder (id, user, rating,\
            language, code_len, runtime, memory, code)\
            VALUES(?,?,?,?,?,?,?,?)')

        data = (i, user[i], rating[i], language[i],
                code_len[i], runtime[i], memory[i], code[i])

        cur.execute(sql, data)

def set_db(contest, problem):
    for roop in range(int(PEOPLE_NUM/20)):

        url = 'https://atcoder.jp/contests/abc' + contest + '/submissions?f.Task=abc' + contest + '_' + problem + '&f.LanguageName=&f.Status=AC&f.User=&page=' + str(roop+1)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'html.parser')

        num = 0
        count = 0

        i = soup.find('tbody')
                
        for j in i.find_all(href = re.compile('/users')):
            user.append(j.text)
            get_rating('https://atcoder.jp' + j.attrs['href'], 0)
            
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
            
        for j in i.find_all(href = re.compile('/contests/abc' + contest + '/submissions/')):
            get_code('https://atcoder.jp' + j.attrs['href'], 0)

    db_name = 'atcoder.db'
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    try:
        create_db(cur)

    except sqlite3.OperationalError:
        cur.execute('DROP TABLE atcoder')
        create_db(cur)

    con.commit()

    cur.close()
    con.close()