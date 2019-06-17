#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pyspark import SparkContext

def createIndex(shapefile):
    import rtree
    import fiona.crs
    import geopandas as gpd
    zones = gpd.read_file(shapefile).to_crs(fiona.crs.from_epsg(4326))
    index = rtree.Rtree()
    for idx,geometry in enumerate(zones.geometry):
        index.insert(idx, geometry.bounds)
    return (index, zones)

def findZone(p, index, zones):
    match = index.intersection((p.x, p.y, p.x, p.y))
    for idx in match:
        if zones.geometry[idx].contains(p):
            return idx


# In[5]:


def getDrugsFromFileToSets(fn1,fn2):
    import re
    w=set()
    with open(fn1) as reader:
        rows = reader.read()
        for row in rows.split("\n"):
            w.add(" ".join(re.split(r'\W+',row)))
    with open(fn2) as reader:
        rows = reader.read()
        for row in rows.split("\n"):
            w.add(" ".join(re.split(r'\W+',row)))
    return w


# In[6]:


def filterDrugs(tweets,drugs_set):
    import re
#     if tweets[1]==0:
#         return False
    lst = re.split(r'\W+',tweets)
    lst = list(filter(lambda x:x!="",lst))
    i=0
    lst1=[]
    for word1 in lst:
        j=i+1
        temp =word1
        if(temp in drugs_set):
            return True
        for word2 in lst[j:]:
            temp = temp+" "+word2
            if(temp in drugs_set):
                return True
        i=i+1
    return False


# In[15]:


def partition(tweetData):
    import pyproj
    import shapely.geometry as geom
    proj = pyproj.Proj(init="epsg:4326", preserve_units=False)
    main_index , main_zone = createIndex('500cities_tracts.geojson')
    drugs_set = getDrugsFromFileToSets('drug_illegal.txt','drug_sched2.txt')
    city_index = None
    for tweet in tweetData:
        tweet_split = tweet.split('|')
        try:
            x = float(tweet_split[2])
            y = float(tweet_split[1])
            point = geom.Point((x,y))
            city_index = findZone(point,main_index,main_zone)
        except:
            pass
        if not city_index:
            pass
            #print(tweet_split[0])
        else:
            if filterDrugs(tweet_split[5],drugs_set):
                yield(main_zone['plctract10'][city_index],main_zone['plctrpop10'][city_index]),1.0


# In[16]:


def mapper(data):
    return (data[0],data[1]),1
def normalizer(data):
    return data[0][0],float(data[1])/float(data[0][1])


# In[23]:


if __name__=='__main__':
    #sc = SparkContext()
    sc.textFile('/data/share/bdm/tweets-100m.csv').mapPartitions(partition).reduceByKey(lambda x,y:x+y).filter(lambda x:int(x[0][1])!=0).map(normalizer).sortBy(lambda x:x[0]).saveAsTextFile("final006")


# In[ ]:





# In[ ]:




