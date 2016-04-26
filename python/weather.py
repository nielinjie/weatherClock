import json
import sys
import urllib2
from datetime import datetime, timedelta


class Forecast:
    def __init__(self, weathers, now):
        self.weathers = weathers
        self.now = now

    def forecast(self):
        def tomorrow(now, time):
            nextMidleNight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)
            return (time > nextMidleNight) and (time < nextMidleNight + timedelta(1))

        def today(now, time):
            nextMidleNight = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)
            return (time > now) and (time < nextMidleNight)

        def fromW(ws):
            if len(ws) == 0:
                raise ValueError('no weather forecast found')
            wr = fromWeather(ws[0])
            for w in ws[1:]:
                wr = wr.aggregate(w)
            return wr

        # aggregate tomorrow
        allTomorrow = filter(lambda w: tomorrow(self.now, w.time), self.weathers)
        allToday = filter(lambda w: today(self.now, w.time), self.weathers)
        return {'tomorrow': fromW(allTomorrow), 'today': fromW(allToday)}


def fromWeather(w):
    return WeatherResult([w.code], w.temp, w.temp)


class WeatherResult:
    def __init__(self, codes, maxTemp, minTemp):
        self.codes = codes
        self.maxTemp = maxTemp
        self.minTemp = minTemp

    def aggregate(self, b):
        return WeatherResult(self.codes + [b.code], max(self.maxTemp, b.temp), min(self.minTemp, b.temp))

    def warning(self):
        for c in self.codes:
            warningHeads = [2, 3, 5, 6, 9]
            # http://openweathermap.org/weather-conditions
            if (c / 100 in warningHeads) and not (c > 950):
                return c
        return 0

    def __str__(self):
        return "%s - %s - %s" % (self.codes, self.maxTemp, self.minTemp)

    __repr__ = __str__


class Weather:
    def __init__(self, time, code, temp):
        self.time = time
        self.code = code
        self.temp = temp

    def __str__(self):
        return "%s - %s - %s" % (self.time, self.code, self.temp)

    __repr__ = __str__


url = 'http://api.openweathermap.org/data/2.5/forecast?q=Chengdu,cn&mode=json&units=metric&APPID=' + sys.argv[1]
print url
content = urllib2.urlopen(url)
data = json.load(content)

weathers = []

for d in data['list'][0:19]:
    date = datetime.fromtimestamp(d['dt'])
    weathers += [Weather(date, d['weather'][0]['id'], d['main']['temp'])]

forecast = Forecast(weathers, datetime.now())

fore = forecast.forecast()
print fore
print fore['tomorrow'].warning()
