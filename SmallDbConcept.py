import psycopg2
import sys
import math
import random
import numpy
import tables

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


rownr = 2000
matrixrownr = rownr * pow(math.log(rownr), 2)

fileName = 'smallconcept.h5'
shape = (int(matrixrownr),rownr + 1)
atom = tables.UInt32Atom()
filters = tables.Filters(complevel=5, complib='zlib')
h5f = tables.open_file(fileName, 'w')
ca = h5f.create_carray(h5f.root, 'carray', atom, shape, filters=filters)

#matrix = numpy.zeros(shape=(int(matrixrownr),rownr))
#vector = []
vfileName = 'smallconceptresult.h5'
vshape = (int(matrixrownr), 2)
vh5f = tables.open_file(vfileName, 'w')
vca = vh5f.create_carray(vh5f.root, 'carray', atom, vshape, filters=filters)

efileName = 'smallconceptexpected.h5'
eshape = (rownr, 2)
eh5f = tables.open_file(efileName, 'w')
eca = h5f.create_carray(eh5f.root, 'carray', atom, eshape, filters=filters)


#querrying
con = None
try:

    con = psycopg2.connect(database='taxi', user='postgres', password='postgres')
    cur = con.cursor()

    k = 1
    while k < rownr:
        expectedquery = 'SELECT trip_time_in_secs FROM jan08 WHERE id = ' + str(k)
        print(k)
        cur.execute(expectedquery)
        value = cur.fetchone()
        eca[k, 0] = k
        if value[0] < 550:
            eca[k, 1] = 1
        else:
            eca[k, 1] = 0
        k = k + 1



    # cp builder loop
    for i in range(int(matrixrownr)):
        # random 5-15% (1-2)
        attributenr = random.randint(1, 3)
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
        firstattributecurrentmin = firstattributecurrentmin * 0.1
        firstattributecurrentmax = firstattributecurrentmax * 2
        if attributenr == 2:
            secondattributecurrentmin = numpy.random.normal((secondattribute.maximum - secondattribute.minimum) / 2, 1)
            secondattributecurrentmax = numpy.random.normal((secondattribute.maximum - secondattribute.minimum) / 2, 1)
            if secondattributecurrentmax < secondattributecurrentmin:
                temp = secondattributecurrentmin
                secondattributecurrentmin = secondattributecurrentmax
                secondattributecurrentmax = temp
            secondattributecurrentmin = secondattributecurrentmin * 0.1
            secondattributecurrentmax = secondattributecurrentmax * 2
        # building the querry
        querryremote = 'SELECT COUNT(*) FROM jan08 WHERE ' + firstattribute.name + ' BETWEEN ' + str(firstattributecurrentmin) + ' AND ' + str(firstattributecurrentmax)
        if attributenr == 2:
            querryremote = querryremote + ' AND ' + secondattribute.name + ' BETWEEN ' + str( secondattributecurrentmin) + ' AND ' + str(secondattributecurrentmax)
        querryremote = querryremote + ' AND trip_time_in_secs<550'
        querrylocal = 'SELECT id FROM jan08 WHERE ' + firstattribute.name + ' BETWEEN ' + str(firstattributecurrentmin) + ' AND ' + str(firstattributecurrentmax)
        if attributenr == 2:
            querrylocal = querrylocal + ' AND ' + secondattribute.name + ' BETWEEN ' + str(secondattributecurrentmin) + ' AND ' + str(secondattributecurrentmax)
        # querrying local db and filling the matrix
        cur.execute(querrylocal)
        currentrow = []
        print(i)
        ca[i, 0] = i
        print(ca[i, 0])
        j = 1
        while True:
            row = cur.fetchone()
            if row == None:
                break
            while(j <= row[0]):
                #currentrow.append(0)
                #print(row[0])
                #print(j)
                ca[i, j] = 0
               # print(row[0])
               # print(j)
                j = j + 1
            #currentrow.append(1)
            if j<rownr & i<int(matrixrownr):
                ca[i, j] = 1
            j = j + 1
        #matrix[i] = currentrow
        # querrying remote db and filling the vector
        cur.execute(querryremote)
        nr = cur.fetchone()
        vca[i, 0] = i + 1000000
        print(vca[i, 0])
        vca[i, 1] = nr
       # print(i)


   # cur.execute('SELECT MAX(total_amount) FROM jan08')
   # one = cur.fetchall()
   # print(one)

except psycopg2.DatabaseError as e:
    print('Error %s' % e)
    sys.exit(1)

finally:

    if con:
        con.close()

