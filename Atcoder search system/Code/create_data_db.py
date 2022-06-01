from consts import PEOPLE_NUM
from consts import CONTEST_NUM

import sqlite3
import requests
import re
import time
from bs4 import BeautifulSoup

#User Agent
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62'}

user = []      #ユーザ名
rating = []    #レート
language = []  #プログラミング言語
code_len = []  #コード長
runtime = []   #実行時間
memory = []    #メモリ使用量
code = []      #ソースコード

#初期化
def initialization():
    user.clear()
    rating.clear()
    language.clear()
    code_len.clear()
    runtime.clear()
    memory.clear()
    code.clear()

#前処理
def pre_processing(contest, problem):
    int_contest = int(contest)

    if 42 <= int_contest and int_contest <= 50:
        preprocess = 'arc' + str(int_contest+16).zfill(3)
    
    elif 52 <= int_contest and int_contest <= 53:
        preprocess = 'arc' + str(int_contest+15).zfill(3)
    
    elif 55 <= int_contest and int_contest <= 56:
        preprocess = 'arc' + str(int_contest+14).zfill(3)
    
    elif 58 <= int_contest and int_contest <= 60:
        preprocess = 'arc' + str(int_contest+13).zfill(3)

    elif 62 <= int_contest and int_contest <= 63:
        preprocess = 'arc' + str(int_contest+12).zfill(3)
    
    elif 65 <= int_contest and int_contest <= 69:
        preprocess = 'arc' + str(int_contest+11).zfill(3)
    
    elif 71 <= int_contest and int_contest <= 72:
        preprocess = 'arc' + str(int_contest+10).zfill(3)
    
    elif int_contest == 74:
        preprocess = 'arc' + str(int_contest+9).zfill(3)
    
    elif 77 <= int_contest and int_contest <= 78:
        preprocess = 'arc' + str(int_contest+7).zfill(3)
    
    elif 81 <= int_contest and int_contest <= 83:
        preprocess = 'arc' + str(int_contest+5).zfill(3)
    
    elif 86 <= int_contest and int_contest <= 87:
        preprocess = 'arc' + str(int_contest+3).zfill(3)
    
    elif 90 <= int_contest and int_contest <= 95:
        preprocess = 'arc' + str(int_contest+1).zfill(3)

    elif 97 <= int_contest and int_contest <= 98:
        preprocess = 'arc' + contest
    
    elif 101 <= int_contest and int_contest <= 102:
        preprocess = 'arc' + str(int_contest-2).zfill(3)
    
    elif 107 <= int_contest and int_contest <= 108:
        preprocess = 'arc' + str(int_contest-6)
    
    elif int_contest == 111:
        preprocess = 'arc' + str(int_contest-8)
    
    else:
        preprocess = 'abc' + contest + '_' + problem

        return preprocess
    
    if problem == 'c':
        preprocess += '_a'
    else:
        preprocess += '_b' 
    
    return preprocess

#ソースコード取得
def get_code(code_url, count):

    code_html = requests.get(code_url)
    code_soup = BeautifulSoup(code_html.content, 'html.parser')
    for k in code_soup.find_all('pre'):
        if count == 0:
            code.append(k.text)
        count += 1

#レート取得
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

#DB TABLE作成
def create_db(cur, contest, problem):

    cur.execute('CREATE TABLE atcoder_' + contest + '_' + problem + '(id INTEGER, user STRING,\
        rating STRING, language STRING,code_len STRING,\
        runtime STRING, memory STRING, code STRING)')

    #PEOPLE_NUMよりデータ数少ない場合
    if len(user) < PEOPLE_NUM:
        length = len(user)

    else:
        length = PEOPLE_NUM

    for i in range(length):
        sql = ('INSERT INTO atcoder_' + contest + '_' + problem + ' (id, user, rating,\
            language, code_len, runtime, memory, code)\
            VALUES(?,?,?,?,?,?,?,?)')

        data = (i, user[i], rating[i], language[i], code_len[i], runtime[i], memory[i], code[i])

        cur.execute(sql, data)

#DB基本情報
def set_db(cur, contest, problem):
    if (42 <= int(contest) and int(contest) <= 111) and (problem == 'c' or problem == 'd'):
        preprocess = pre_processing(contest, problem)
    
    else:
        preprocess = 'abc' + contest + '_' + problem

    for roop in range(int(PEOPLE_NUM/20)):
        url_str = 'https://atcoder.jp/contests/abc' + contest + '/submissions?f.Task=' + preprocess + \
            '&f.LanguageName=&f.Status=AC&f.User=&page='

        url = url_str + str(roop+1)
        html = requests.get(url, headers=UA)
        soup = BeautifulSoup(html.content, 'html.parser')

        num = 0
        count = 0   

        i = soup.find('tbody')

        if len(soup.select('tbody')) == 0:
            break
                
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
        
        time.sleep(1)
    
    if int(contest) < 20:
        problem = chr(97 + int(problem) -1)

    cur.execute('DROP TABLE IF EXISTS atcoder_' + contest + '_' + problem)
    create_db(cur, contest, problem)

    print('abc' + contest + '_' + problem +': success!')

def main():

    #コンテスト読み込み開始
    START_CONTEST = 241

    for i in range(START_CONTEST, CONTEST_NUM+1):

        db_name = 'atcoder.db'
        con = sqlite3.connect(db_name)
        cur = con.cursor()

        if i < 20:
            alphabet = ['1', '2', '3', '4']

        elif i <= 125:
            alphabet = ['a', 'b', 'c', 'd']

        elif i <= 211:
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f']
        
        else:
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        contest = str(i).zfill(3)
        
        for problem in alphabet:
            initialization()

            set_db(cur, contest, problem)

        con.commit()

        cur.close()
        con.close()

if __name__ == '__main__':
    main()