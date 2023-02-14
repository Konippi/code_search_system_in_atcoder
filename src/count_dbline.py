from consts import CONTEST_NUM
import sqlite3

def count_line(cur, contest, problem):
    if int(contest) < 20:
        problem = chr(97 + int(problem) -1)

    cur.execute('SELECT COUNT(*) FROM atcoder_' + contest + '_' + problem)

    print('abc_' + contest + '_' + problem + ': ' + str(cur.fetchall()))

def main():
    START_PROBLEM = 1

    for i in range(START_PROBLEM, CONTEST_NUM+1):

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
            count_line(cur, contest, problem)

        con.commit()

        cur.close()
        con.close()

if __name__ == '__main__':
    main()