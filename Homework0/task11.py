import sys
import json

if __name__=='__main__':
    with open(sys.argv[1], 'r') as fi:
        data = json.load(fi)
        stations = data['stationBeanList']
        #print('stationName',':','latitude',',','longitude')
        for s in stations:
            print(s['stationName'],':',s['latitude'],',',s['longitude'])


