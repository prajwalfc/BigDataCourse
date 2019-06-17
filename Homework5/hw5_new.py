#!/usr/bin/env python
# coding: utf-8

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

def findZone(p, index, zones):
    match = index.intersection((p.x, p.y, p.x, p.y))
    for idx in match:
        if zones.geometry[idx].contains(p):
            return idx
    return None

def processTrips(pid, records):
    import csv
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
        ls = i.split(',')
        lst=[]
        isAllDigits = True
        try:
            l = [ls[5],ls[6],ls[9],ls[10]]#there is a blank line after header,this try catch handles it.
            lst = list(map(lambda x: float(x),l))#there is a blank line after header,this try catch handles it.
        except IndexError:
            pass
        except ValueError:
            isAllDigits = False
        if(lst and isAllDigits ):
            proj = pyproj.Proj(init="epsg:2263", preserve_units=True)    
            start = geom.Point(proj(float(lst[0]),float(lst[1])))
            end = geom.Point(proj(float(lst[2]),float(lst[3])))
            start_index = findZone(start,index_neighbourhood,zone_neighbourhood)
            end_index = findZone(end,index_boroughs,zone_boroughs)
            if None not in [start_index, end_index] :
                #print(count,boroughs['boroname'][end_index],neighborhoods['neighborhood'][start_index],int(1))
                yield(boroughs['boroname'][end_index],neighborhoods['neighborhood'][start_index],int(1))

if __name__=='__main__':
    sc = SparkContext()
    rdd = sc.textFile('/data/share/bdm/yellow_tripdata_2011-05.csv')
    counts = rdd.mapPartitionsWithIndex(processTrips)
    a = counts.groupBy(lambda x:(x[0],x[1])).mapValues(len)
    from heapq import nlargest
    b=a.map(lambda x:(x[0][0],x[0][1],x[1]))
    result = b.groupBy(lambda x: x[0]).flatMap(lambda g: nlargest(3, g[1], key=lambda x: x[2]))
    result.saveAsTextFile("results")
