#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import geopandas as gpd
# import fiona
# neighborhoods = gpd.read_file('neighborhoods.geojson').to_crs(fiona.crs.from_epsg(2263))
# neighborhoods
# boroughs = gpd.read_file('boroughs.geojson').to_crs(fiona.crs.from_epsg(2263))
# boroughs


# In[2]:

from pyspark import SparkContext
def createIndex(shapefile):
    import rtree
    import fiona.crs
    import geopandas as gpd
    zones = gpd.read_file(shapefile).to_crs(fiona.crs.from_epsg(2263))
    index = rtree.Rtree()
    for idx,geometry in enumerate(zones.geometry):
        index.insert(idx, geometry.bounds)
    return (index, zones)


# In[3]:


def findZone(p, index, zones):
    match = index.intersection((p.x, p.y, p.x, p.y))
    for idx in match:
        if zones.geometry[idx].contains(p):
            return idx
    return None


# In[4]:


def processTrips(pid, records):
    import csv
    count =0
    import pyproj
    import shapely.geometry as geom
    import geopandas as gpd
    import fiona
    neighborhoods = gpd.read_file('neighborhoods.geojson').to_crs(fiona.crs.from_epsg(2263))
    boroughs = gpd.read_file('boroughs.geojson').to_crs(fiona.crs.from_epsg(2263))
    index_neighbourhood,zone_neighbourhood = createIndex('neighborhoods.geojson')
    index_boroughs,zone_boroughs = createIndex('boroughs.geojson')
    if pid ==0:
        next(records)
    for i in records:
        lst = i.split(',')
        lst=[]
        try:
            lst = [ls[5],ls[6],ls[9],ls[10]]#there is a blank line after header,this try catch handles it.
        except IndexError:
             pass
        if(lst and ('NULL' not in lst)):
            proj = pyproj.Proj(init="epsg:2263", preserve_units=True)    
            start = geom.Point(proj(float(lst[0]),float(lst[1])))
            end = geom.Point(proj(float(lst[2]),float(lst[3])))
            start_index = findZone(start,index_neighbourhood,zone_neighbourhood)
            start_index = findZone(start,index_neighbourhood,zone_neighbourhood)
            end_index = findZone(end,index_boroughs,zone_boroughs)
            if None not in [start_index, end_index] :
                #print(count,boroughs['boroname'][end_index],neighborhoods['neighborhood'][start_index],int(1))
                yield(boroughs['boroname'][end_index],neighborhoods['neighborhood'][start_index],int(1))


# In[11]:


# rdd = sc.textFile('yellow.csv')
# counts = rdd.mapPartitionsWithIndex(processTrips)
# a = counts.groupBy(lambda x:(x[0],x[1])).mapValues(len)
# a.take(6)


# In[12]:


# from heapq import nlargest
# b=a.map(lambda x:(x[0][0],x[0][1],x[1]))
# result = b.groupBy(lambda x: x[0]).flatMap(lambda g: nlargest(3, g[1], key=lambda x: x[2])).collect()


# In[13]:


#print(result)


# In[10]:


if __name__=='__main__':
    sc = SparkContext()
    rdd = sc.textFile('yellow.csv')
    counts = rdd.mapPartitionsWithIndex(processTrips)
    a = counts.groupBy(lambda x:(x[0],x[1])).mapValues(len)
    from heapq import nlargest
    b=a.map(lambda x:(x[0][0],x[0][1],x[1]))
    result = b.groupBy(lambda x: x[0]).flatMap(lambda g: nlargest(3, g[1], key=lambda x: x[2]))
    result.saveAsTextFile("output")
    


# In[ ]:




