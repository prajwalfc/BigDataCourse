#!/usr/bin/env python
# coding: utf-8

# In[1]:


sc


# In[2]:


def filterBike(pid,records):
    if pid ==0:
        next(records)
    for record in records:
        fields =  record.split(',')
        if(fields[6]=='Greenwich Ave & 8 Ave' and fields[3].startswith('2015-02-01')):
            yield(fields[3][:19],1)


# In[3]:


bike = sc.textFile('citibike.csv')
bike.take(1)[0].split(',')


# In[4]:


matchedBike = bike.mapPartitionsWithIndex(filterBike)
matchedBike.take(2)


# In[5]:


# def filterTaxi(pid,lines):
#     if pid == 0:
#         next(lines)
#     import pyproj
#     proj = pyproj.Proj(init = 'epsg:2263',preserver_units = True)
#     station = proj(-74.00263761,40.73901691)
#     radius = 1320**2
#     for trip in lines:
#         fields  = trip.split(',')
#         if 'NULL' in fields[4:6]: continue
#         dropoff  = proj(fields[5],fields[4])
#         distance = ((station[0]-dropoff[0])**2 + (station[1] - dropoff[1])**2)
#         if distance<=radius:
#             yield(fields[1][:19],0)


# In[6]:


def filterTaxi(pid, lines):
   if pid ==0:
       next(lines)
   import pyproj
   proj = pyproj.Proj(init='epsg:2263', preserve_units=True)
   station = proj(-74.00263761, 40.73901691)
   radius = 1320**2
   for trip in lines:
       fields = trip.split(',')
       if 'NULL' in fields[4:6]: continue
       dropoff = proj(fields[5], fields[4])
       distance = ((station[0] - dropoff[0])**2 + (station[1] - dropoff[1])**2)
       if distance <= radius:
           yield (fields[1][:19],0)

taxi = sc.textFile('yellow.csv')
taxi.take(2)[1].split(',')
matchedTaxi = taxi.mapPartitionsWithIndex(filterTaxi)
matchedTaxi.take(2)


# In[7]:


allTrips = (matchedBike+matchedTaxi).sortByKey().cache()


# In[8]:


def connectTrips(_, records):
   import datetime
   lastTaxiTime = None
   count = 0
   for dt, mode in records:
       t = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
       if mode == 1:
           if lastTaxiTime != None:
               diff = (t-lastTaxiTime).total_seconds()
               if  0 <= diff <= 10:
                   count += 1
       else:
           lastTaxiTime = t
   yield count


allTrips.mapPartitionsWithIndex(connectTrips).reduce(lambda x,y: x+y)


# In[ ]:




