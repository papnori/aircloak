import psycopg2
import sys
import math
import random
import numpy

class Attribute:

    def __init__(self, name, mi, ma):
        self.name = name
        self.minimum = mi
        self.maximum = ma

#creating attributes
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
attributes = [ratecode, passenger, triptime, distance, pickuplong, pickuplat, dropofflong, dropofflat, fare, surcharge, tip, toll, total]


rownr = 440257
matrixrownr = rownr * pow(math.log(rownr), 2)
matrix = []
vector = []
attributenrvector = []


#querrying
con = None
try:

    con = psycopg2.connect(database='taxi', user='postgres', password='postgres')
    cur = con.cursor()

    # cp builder loop
    for i in range(int(matrixrownr)):
        # random 5-15% (1-2)
        attributenr = random.randint(1, 3)
        # filling attributenrvector
        attributenrvector.append(attributenr)
        # choosing which attributes to querry
        firstattribute = attributes[random.randint(0, 12)]
        if attributenr == 2:
            secondattribute = attributes[random.randint(0, 12)]
            while secondattribute == firstattribute:
                secondattribute = attributes[random.randint(0, 12)]
        # normal distribution min max
        firstattributecurrentmin = numpy.random.normal((firstattribute.maximum - firstattribute.minimum) / 2, 1)
        firstattributecurrentmax = numpy.random.normal((firstattribute.maximum - firstattribute.minimum) / 2, 1)
        if firstattributecurrentmax < firstattributecurrentmin:
            temp = firstattributecurrentmin
            firstattributecurrentmin = firstattributecurrentmax
            firstattributecurrentmax = temp
        if attributenr == 2:
            secondattributecurrentmin = numpy.random.normal((secondattribute.maximum - secondattribute.minimum) / 2, 1)
            secondattributecurrentmax = numpy.random.normal((secondattribute.maximum - secondattribute.minimum) / 2, 1)
            if secondattributecurrentmax < secondattributecurrentmin:
                temp = secondattributecurrentmin
                secondattributecurrentmin = secondattributecurrentmax
                secondattributecurrentmax = temp
        # building the querry
        querryremote = 'SELECT COUNT(*) FROM jan08 WHERE ' + firstattribute.name + ' BETWEEN ' + str(firstattributecurrentmin) + ' AND ' + str(firstattributecurrentmax)
        if attributenr == 2:
            querryremote = querryremote + ' AND ' + secondattribute.name + ' BETWEEN ' + str( secondattributecurrentmin) + ' AND ' + str(secondattributecurrentmax)
        querrylocal = 'SELECT id FROM jan08 WHERE ' + firstattribute.name + ' BETWEEN ' + str(firstattributecurrentmin) + ' AND ' + str(firstattributecurrentmax)
        if attributenr == 2:
            querrylocal = querrylocal + ' AND ' + secondattribute.name + ' BETWEEN ' + str(secondattributecurrentmin) + ' AND ' + str(secondattributecurrentmax)
        # querrying local db and filling the matrix
        cur.execute(querrylocal)
        currentrow = []
        j = 0
        while True:
            row = cur.fetchone()
            if row == None:
                break
            while(j < row[0]):
                currentrow.append(0)
                j = j + 1
            currentrow.append(1)
            j = j + 1
        matrix.append(currentrow)
         # querrying remote db and filling the vector

   # cur.execute('SELECT MAX(total_amount) FROM jan08')
   # one = cur.fetchall()
   # print(one)

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)

finally:

    if con:
        con.close()

