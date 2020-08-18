import sqlite3

with sqlite3.connect('base.db') as db:
    cur = db.cursor()

    #cur.execute(u"""INSERT INTO base VALUES (403689973, 'Vladyslav', 'None', 'QuantumaStelata', 1390, 3, 'voice/403689972/', '{1:2}', 'None')""")
    cur.execute(u"""SELECT timezone FROM base WHERE fname='Vladyslav'""")
    print (cur.fetchone()[0])
