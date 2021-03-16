import sqlite3

conn = sqlite3.connect(input())
condition1 = str(input())
condition2 = str(input())
order = str(input())

c = conn.cursor()
c.execute('SELECT condition FROM Talks WHERE (' + condition1 + ') AND (' + condition2 + ') ORDER BY ' + order + ' ASC;')
rows = c.fetchall()
for r in rows:
    print(r[0])
