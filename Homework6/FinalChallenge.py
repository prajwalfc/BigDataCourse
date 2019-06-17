#!/usr/bin/env python
# coding: utf-8

# In[7]:


from pyspark import SparkContext


# In[8]:


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


# In[14]:


def getDrugsFromFileToSet(fn1,fn2):
    w=set()
    phrase = set()
    with open(fn1) as reader:
        rows = reader.read()
        for row in rows.split("\n"):
            if " " in row:
                phrase.add(row.strip())
            else:
                w.add(row.strip())
    with open(fn2) as reader:
        rows = reader.read()
        for row in rows.split("\n"):
            if " " in row:
                phrase.add(row.strip())
            else:
                w.add(row.strip())
    return w,phrase
# def lineToBigrams(tweets):
#     import nltk
#     tweet_bigram = ()
#     tweet_token = ()
#     for tweet in tweets[0][3:]:
#         tweet_token+=tuple(tweet.split(" "))
#         tweet_bigram += tuple(nltk.bigrams(nltk.word_tokenize(tweet)))
#     tweet_bigram_refine = tuple(map(lambda x: " ".join(x).lower(),tweet_bigram))
#     tweet_token_refine = tuple(map(lambda x: x.lower(),tweet_token))
#     return (tweet_token_refine+tweet_bigram_refine)
# def testToBigram(tweets):
#     drug_tweet = 0
#     tweet_token = lineToBigrams(tweets)
#     drug_name_set = getDrugsFromFileToSet('drug_illegal.txt','drug_sched2.txt')
#     if(drug_name_set.intersection(set(tweet_token))):
#         drug_tweet = 1
#     return tweets[0][1:3],drug_tweet
# def filterDrugs(tweets):
#     import re
#     a,b = getDrugsFromFileToSet('drug_illegal.txt','drug_sched2.txt')
#     for tweet in tweets[2]:
#         for drug in b:
#             sets = re.findall(r' '+drug+' |^'+drug+' | '+drug+'$',tweet)
#             if sets:
#                 return True
#     return False
def filterDrugs(tweets):
    import re
    a,b = getDrugsFromFileToSet('drug_illegal.txt','drug_sched2.txt')
    for tweet in tweets[2]:
        sets = a.intersection(set(tweet.split(" ")))
        if sets:
            print("word----------------",sets)
            return True
        else:
            for drug in b:
                if drug in tweet:
                    print("phrase--------------",drug)
                    return True
    return False


# In[15]:


def partition(tweetData):
    import pyproj
    import shapely.geometry as geom
    proj = pyproj.Proj(init="epsg:4326", preserve_units=False)
    main_index , main_zone = createIndex('500cities_tracts.geojson')
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
            yield(main_zone['plctract10'][city_index],main_zone['plctrpop10'][city_index],tweet_split[5:])


# In[11]:


def mapper(data):
    return (data[0],data[1]),1
def normalizer(data):
    return data[0][0],data[1]/data[0][1]


# In[16]:


if __name__=='__main__':
    #sc = SparkContext()
    rdd = sc.textFile('input.txt')
    rdd.mapPartitions(partition)        .filter(filterDrugs)        .map(mapper)        .reduceByKey(lambda x,y:x+y)        .map(normalizer)        .saveAsTextFile("res_opt19")


# In[ ]:




