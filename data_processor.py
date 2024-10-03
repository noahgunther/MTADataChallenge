import requests
import json
from datetime import datetime, timedelta

def dateDeconstructor(dateString):
    year = int(dateString[:4])
    month = int(dateString[5:7])
    day = int(dateString[8:10])
    hour = int(dateString[11:13])
    return datetime(year, month, day, hour, 0, 0, 0)

def longDateConstructor(date):
    weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    month = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    nth = 'th'
    dayInt = date.day
    dayString = str(dayInt)
    tenToNineteen = dayString[:1] == '1' and dayInt > 9
    if not (tenToNineteen):
        if (dayString[-1:] == '1'): nth = 'st'
        elif (dayString[-1:] == '2'): nth = 'nd'
        elif (dayString[-1:] == '3'): nth = 'rd'

    return weekday[date.weekday()] + ", " + month[date.month - 1] + " " + dayString + nth + ", " + str(date.year)

def queryDateConstructor(date):
    dateConstruct = str(date)[:10]
    timeConstruct = str(date)[11:19]
    return dateConstruct + "T" + timeConstruct


# Get most recent available hourly set day
url = 'https://data.ny.gov/resource/wujg-7c2s.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$order=transit_timestamp+DESC&$limit=1'
data = requests.get(url).json()
dateMostRecent = dateDeconstructor(data[0]['transit_timestamp'])
dateWeekStart = dateMostRecent - timedelta(days=7)
dateYearStart = dateMostRecent - timedelta(days=365)

dateMostRecentLong = longDateConstructor(dateMostRecent)
dateWeekStartLong = longDateConstructor(dateWeekStart)
dateYearStartLong = longDateConstructor(dateYearStart)

# Get year of data from daily ridership set 
url = "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$limit=365&$order=date+DESC&$where=date+between+%27" + queryDateConstructor(dateYearStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27"
data = requests.get(url).json()

# Weekly ridership from daily data
subwayWeeklyRidership = 0
subwayMaxDailyRidershipWeekly = 0
subwayMaxDailyDateWeekly = ''
busWeeklyRidership = 0
busMaxDailyRidershipWeekly = 0
busMaxDailyDateWeekly = ''
for i in range(7):
    subwayDailyRidership = int(data[i]['subways_total_estimated_ridership'])
    busDailyRidership = int(data[i]['buses_total_estimated_ridersip'])

    subwayWeeklyRidership += subwayDailyRidership
    if (subwayDailyRidership > subwayMaxDailyRidershipWeekly):
        subwayMaxDailyRidershipWeekly = subwayDailyRidership
        subwayMaxDailyDateWeekly = data[i]['date']

    busWeeklyRidership += busDailyRidership
    if (busDailyRidership > busMaxDailyRidershipWeekly):
        busMaxDailyRidershipWeekly = busDailyRidership
        busMaxDailyDateWeekly = data[i]['date']

data = {
    'last_cached': str(datetime.now()),
    'dateMostRecent': dateMostRecentLong,
    'dateWeekStart': dateWeekStartLong,
    'dateYearStart': dateYearStartLong,
    'subwayWeeklyRidership': subwayWeeklyRidership,
    'subwayMaxDailyRidershipWeekly': subwayMaxDailyRidershipWeekly,
    'subwayMaxDailyDateWeekly': subwayMaxDailyDateWeekly,
    'busWeeklyRidership': busWeeklyRidership,
    'busMaxDailyRidershipWeekly': busMaxDailyRidershipWeekly,
    'busMaxDailyDateWeekly': busMaxDailyDateWeekly
}

print(data)

# Write json
#with open('./data/data.json', 'w') as f:
#    json.dump(data, f)