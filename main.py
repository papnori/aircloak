import psycopg2
import sys

con = None
try:

    con = psycopg2.connect(database='bank', user='postgres', password='admin')
    cur = con.cursor()
    #cur.execute('SELECT version()')
    cur.execute('SELECT * FROM clients')
    one = cur.fetchall()
    print(one)

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)

finally:

    if con:
        con.close()

