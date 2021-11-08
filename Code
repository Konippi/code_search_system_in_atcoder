import sqlite3  #SQLite
import requests  #HTMLにアクセス&データ取得
import re  #compile関数を用いる
from bs4 import BeautifulSoup  #HTMLから特定のデータを抽出する

def get_code(code_url, num2):

    code_html = requests.get(code_url)
    code_soup = BeautifulSoup(code_html.content, 'html.parser')
    for k in code_soup.find_all('pre'):
        if num2 == 0:
            code.append(k.text)
        num2 += 1

def get_rating(user_url, num3, i):

    user_html = requests.get(user_url)
    user_soup = BeautifulSoup(user_html.content, 'html.parser')
    
    for k in user_soup.find_all('span', class_ = re.compile('user-')):
        if num3 == 1:
            user[i]+=(' ' + k.text)
        num3 += 1

def print_out():

    print('コンテスト名:')
    print(title.text, '\n')

    print('問題:')
    print(problem.text)
    print('https://atcoder.jp' + problem.attrs['href'], '\n')

    print("提出日時:")
    for i in date:
        print(i)
    print("")

    print("ユーザ:")
    for i in user:
        print(i)
    print("")

    print("言語:")
    for i in language:
        print(i)
    print("")

    print("コード長:")
    for i in code_len:
        print(i)
    print("")

    print("実行時間:")
    for i in runtime:
        print(i)
    print("")

    print("メモリ:")
    for i in memory:
        print(i)
    print("")

    print("ソースコード:")
    for i in code:
        print(i)
    print("")

url = 'https://atcoder.jp/contests/abc100/submissions?f.Task=abc100_b&f.LanguageName=&f.Status=AC&f.User='
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')

date = []
user = []
language = []
code_len = []
runtime = []
memory = []
code = []
num = 0
m = 0

title = soup.find('a', class_ = 'contest-title')
problem = soup.find(href = re.compile('/abc100_b'))

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
    
print_out()
