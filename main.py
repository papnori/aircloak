import psycopg2
import sys

class Attribute:

    def __init__(self, name, mi, ma):
        self.name = name
        self.minimum = mi
        self.maximum = ma

con = None
try:

    con = psycopg2.connect(database='taxi', user='postgres', password='postgres')
    cur = con.cursor()

    cur.execute('SELECT MAX(total_amount) FROM jan08')
    one = cur.fetchall()
    print(one)

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)

finally:

    if con:
        con.close()

