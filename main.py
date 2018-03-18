import psycopg2
import sys

con = None
try:

    con = psycopg2.connect(database='taxi', user='postgres', password='postgres')
    cur = con.cursor()

    cur.execute('SELECT COUNT(*) FROM jan08')
    one = cur.fetchall()
    print(one)

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)

finally:

    if con:
        con.close()

