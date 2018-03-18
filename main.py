import psycopg2
import sys

class Attribute:

    def __init__(self, name, mi, ma):
        self.name = name
        self.minimum = mi
        self.maximum = ma

con = None
ratecode = Attribute('rate_code', 0, 6)
passenger = Attribute('passenger_count', 0, 6)
triptime = Attribute('trip_time_in_secs', 0, 10320)
distance = Attribute('trip_distance', 0, 97.3)
pickuplong = Attribute('pickup_longitude', -735.3, 0.0)
pickuplat = Attribute('pickup_latitude', -3127.7, 3210.4)
dropofflong = Attribute('dropoff_longitude', -2134.8, 1347.5)
dropofflat = Attribute('dropoff_latitude', -0.6, 898.3)
fare = Attribute('fare_amount', 2.5, 300.0)
surcharge = Attribute('surcharge', 0.0, 3.0)
tip = Attribute('tip_amount', 0.0, 165.0)
toll = Attribute('tolls_amount', 0.0, 20.0)
total = Attribute('total_amount', 2.5, 370.5)
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

