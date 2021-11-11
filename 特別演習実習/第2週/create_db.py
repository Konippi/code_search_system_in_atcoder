import sqlite3

db_name = 'atcoder.db'
con = sqlite3.connect(db_name)
cur = con.cursor()

cur.execute('CREATE TABLE atcoder(id INTEGER ,date STRING,\
    user STRING, rating STRING, language STRING,code_len STRING,\
    runtime STRING, memory STRING, code STRING)')

con.commit()
con.close()
