import urllib2
import json
from datetime import datetime,timedelta
import pprint

class Forecast:
    def __init__(self,weathers,now):
        self.weathers =  weathers
        self.now = now

    def forecast(self):
        def fromW(ws):
            if len(ws) == 0:
                 raise ValueError('no weather forecast found')
            wr =fromWeather(ws[0])
            for w in ws[1:]:
                wr = wr.aggregate(w)
            return wr
        #aggregate tomorrow
        allTomorrow = filter(lambda w: self.tomorrow(self.now, w.time) ,self.weathers)
        allToday = filter(lambda w: self.today(self.now, w.time) ,self.weathers)
        return {'tomorrow':fromW(allTomorrow),'today':fromW(allToday)}

    def tomorrow(self,now,time):
        nextMidleNight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)
        return (time > nextMidleNight) and (time < nextMidleNight + timedelta(1))
    def today(self,now,time):
        nextMidleNight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)
        return (time > now) and (time < nextMidleNight)


def fromWeather(w):
    return WeatherResult([w.name],w.temp,w.temp)
class WeatherResult:
    def __init__(self,names,maxTemp,minTemp):
        self.names= names
        self.maxTemp = maxTemp
        self.minTemp = minTemp
    def aggregate(self,b):
        return WeatherResult(self.names+[b.name],max(self.maxTemp,b.temp),min(self.minTemp,b.temp))
    def __str__(self):
        return "%s - %s - %s" % (self.names, self.maxTemp, self.minTemp)
    __repr__ = __str__



class Weather:
    def __init__(self,time,name,temp):
        self.time = time
        self.name = name
        self.temp = temp
    def __str__(self):
        return "%s - %s - %s" % (self.time, self.name, self.temp)
    __repr__ = __str__




url = 'http://api.openweathermap.org/data/2.5/forecast?q=Chengdu,cn&mode=json&units=metric&APPID=fc79f41e5597da2194a280b4c1dcefd9'

content = urllib2.urlopen(url)
data = json.load( content)

weathers = []

for d in data['list'][0:19]:
    date = datetime.fromtimestamp(d['dt'])
    weathers += [Weather(date,d['weather'][0]['main'],d['main']['temp'])]

forecast =  Forecast(weathers,datetime.now())

try:
    print forecast.forecast()
except:
    pass
