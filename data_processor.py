'''This script runs once daily at https://gunthern.pythonanywhere.com to retrieve, calculate and cache site data for https://noahgunther.com/mta'''

import requests
import json
from datetime import datetime, timedelta

weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def dateDeconstructor(dateString):
    year = int(dateString[:4])
    month = int(dateString[5:7])
    day = int(dateString[8:10])
    hour = int(dateString[11:13])
    return datetime(year, month, day, hour, 0, 0, 0)

def longDateConstructor(date):
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
url = "https://data.ny.gov/resource/wujg-7c2s.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$order=transit_timestamp+DESC&$limit=1"
data = requests.get(url).json()
dateMostRecent = dateDeconstructor(data[0]['transit_timestamp'])
dateWeekStart = dateMostRecent - timedelta(days=7)
dateYearStart = dateMostRecent - timedelta(days=365)

dateMostRecentLong = longDateConstructor(dateMostRecent)
dateWeekStartLong = longDateConstructor(dateWeekStart)
dateYearStartLong = longDateConstructor(dateYearStart)

# Get latest year of data from daily ridership set 
url = "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$limit=365&$order=date+DESC&$where=date+between+%27" + queryDateConstructor(dateYearStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27"
data = requests.get(url).json()

# Latest week of ridership from daily data
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
        subwayMaxDailyDateWeekly = longDateConstructor(dateDeconstructor(data[i]['date']))

    busWeeklyRidership += busDailyRidership
    if (busDailyRidership > busMaxDailyRidershipWeekly):
        busMaxDailyRidershipWeekly = busDailyRidership
        busMaxDailyDateWeekly = longDateConstructor(dateDeconstructor(data[i]['date']))

# Latest year of ridership from daily data
subwayYearlyRidership = 0
subwayDaysOfWeekTally = [0,0,0,0,0,0,0]
subwayDaysOfWeekRidership = [0,0,0,0,0,0,0]
busYearlyRidership = 0
busDaysOfWeekTally = [0,0,0,0,0,0,0]
busDaysOfWeekRidership = [0,0,0,0,0,0,0]
for d in data:
    subwayDailyRidership = int(d['subways_total_estimated_ridership'])
    busDailyRidership = int(d['buses_total_estimated_ridersip'])
                
    subwayYearlyRidership += subwayDailyRidership
    busYearlyRidership += busDailyRidership

    day = longDateConstructor(dateDeconstructor(d['date']))[:3]
    if day == 'Mon':
        subwayDaysOfWeekTally[0] += 1; 
        subwayDaysOfWeekRidership[0] += subwayDailyRidership
        busDaysOfWeekTally[0] += 1; 
        busDaysOfWeekRidership[0] += busDailyRidership
    elif day == 'Tue':
        subwayDaysOfWeekTally[1] += 1; 
        subwayDaysOfWeekRidership[1] += subwayDailyRidership
        busDaysOfWeekTally[1] += 1; 
        busDaysOfWeekRidership[1] += busDailyRidership
    elif day == 'Wed':
        subwayDaysOfWeekTally[2] += 1; 
        subwayDaysOfWeekRidership[2] += subwayDailyRidership
        busDaysOfWeekTally[2] += 1; 
        busDaysOfWeekRidership[2] += busDailyRidership
    elif day == 'Thu':
        subwayDaysOfWeekTally[3] += 1; 
        subwayDaysOfWeekRidership[3] += subwayDailyRidership
        busDaysOfWeekTally[3] += 1; 
        busDaysOfWeekRidership[3] += busDailyRidership
    elif day == 'Fri':
        subwayDaysOfWeekTally[4] += 1; 
        subwayDaysOfWeekRidership[4] += subwayDailyRidership
        busDaysOfWeekTally[4] += 1; 
        busDaysOfWeekRidership[4] += busDailyRidership
    elif day == 'Sat':
        subwayDaysOfWeekTally[5] += 1; 
        subwayDaysOfWeekRidership[5] += subwayDailyRidership
        busDaysOfWeekTally[5] += 1; 
        busDaysOfWeekRidership[5] += busDailyRidership
    elif day == 'Sun':
        subwayDaysOfWeekTally[6] += 1; 
        subwayDaysOfWeekRidership[6] += subwayDailyRidership
        busDaysOfWeekTally[6] += 1; 
        busDaysOfWeekRidership[6] += busDailyRidership

subwayMaxAnnualDay = ''
subwayMaxAnnualDayRidership = 0
subwayMaxAnnualDayTally = 0
subwayMaxAnnualDayMeanRidership = 0
subwayMinAnnualDay = ''
subwayMinAnnualDayRidership = 0
subwayMinAnnualDayTally = 0
subwayMinAnnualDayMeanRidership = 0
for i in range(7):
    if subwayDaysOfWeekRidership[i] > subwayMaxAnnualDayRidership:
        subwayMaxAnnualDayRidership = subwayDaysOfWeekRidership[i]
        subwayMaxAnnualDayTally = subwayDaysOfWeekTally[i]
        subwayMaxAnnualDay = weekday[i]
    if subwayMinAnnualDayRidership == 0 or subwayDaysOfWeekRidership[i] < subwayMinAnnualDayRidership:
        subwayMinAnnualDayRidership = subwayDaysOfWeekRidership[i]
        subwayMinAnnualDayTally = subwayDaysOfWeekTally[i]
        subwayMinAnnualDay = weekday[i]        
subwayMaxAnnualDayMeanRidership = subwayMaxAnnualDayRidership / subwayMaxAnnualDayTally
subwayMinAnnualDayMeanRidership = subwayMinAnnualDayRidership / subwayMinAnnualDayTally

busMaxAnnualDay = ''
busMaxAnnualDayRidership = 0
busMaxAnnualDayTally = 0
busMaxAnnualDayMeanRidership = 0
busMinAnnualDay = ''
busMinAnnualDayRidership = 0
busMinAnnualDayTally = 0
busMinAnnualDayMeanRidership = 0
for i in range(7):
    if busDaysOfWeekRidership[i] > busMaxAnnualDayRidership:
        busMaxAnnualDayRidership = busDaysOfWeekRidership[i]
        busMaxAnnualDayTally = busDaysOfWeekTally[i]
        busMaxAnnualDay = weekday[i]
    if busMinAnnualDayRidership == 0 or busDaysOfWeekRidership[i] < busMinAnnualDayRidership:
        busMinAnnualDayRidership = busDaysOfWeekRidership[i]
        busMinAnnualDayTally = busDaysOfWeekTally[i]
        busMinAnnualDay = weekday[i]   
busMaxAnnualDayMeanRidership = busMaxAnnualDayRidership / busMaxAnnualDayTally
busMinAnnualDayMeanRidership = busMinAnnualDayRidership / busMinAnnualDayTally

# Get latest week of data from hourly subway / tram set

# Tram
url = "https://data.ny.gov/resource/wujg-7c2s.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&transit_mode=tram&$where=transit_timestamp+between%27" + queryDateConstructor(dateWeekStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27&$order=transit_timestamp+DESC&$limit=5000"
data = requests.get(url).json()
tramWeeklyRidership = 0
tramDailyRidership = [0,0,0,0,0,0,0]
tramMaxDailyRidershipWeekly = 0
tramMaxDailyDateWeekly = ''

for d in data:
    tramRidership = int(float(d['ridership']))
    tramWeeklyRidership += tramRidership
    date = longDateConstructor(dateDeconstructor(d['transit_timestamp']))
    if date[:3] == 'Mon':
        tramDailyRidership[0] += tramRidership
        if tramDailyRidership[0] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[0]
            tramMaxDailyDateWeekly = date
    elif date[:3] == 'Tue':
        tramDailyRidership[1] += tramRidership
        if tramDailyRidership[1] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[1]
            tramMaxDailyDateWeekly = date
    elif date[:3] == 'Wed':
        tramDailyRidership[2] += tramRidership
        if tramDailyRidership[2] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[2]
            tramMaxDailyDateWeekly = date
    elif date[:3] == 'Thu':
        tramDailyRidership[3] += tramRidership
        if tramDailyRidership[3] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[3]
            tramMaxDailyDateWeekly = date
    elif date[:3] == 'Fri':
        tramDailyRidership[4] += tramRidership
        if tramDailyRidership[4] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[4]
            tramMaxDailyDateWeekly = date
    elif date[:3] == 'Sat':
        tramDailyRidership[5] += tramRidership
        if tramDailyRidership[5] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[5]
            tramMaxDailyDateWeekly = date
    elif date[:3] == 'Sun':
        tramDailyRidership[6] += tramRidership
        if tramDailyRidership[6] > tramMaxDailyRidershipWeekly:
            tramMaxDailyRidershipWeekly = tramDailyRidership[6]
            tramMaxDailyDateWeekly = date

# Write data to json
data = {
    'last_cached': str(datetime.now()),
    'dateMostRecent': dateMostRecentLong,
    'dateWeekStart': dateWeekStartLong,
    'dateYearStart': dateYearStartLong,
    'subwayWeeklyRidership': subwayWeeklyRidership,
    'subwayYearlyRidership': subwayYearlyRidership,
    'subwayMaxDailyRidershipWeekly': subwayMaxDailyRidershipWeekly,
    'subwayMaxDailyDateWeekly': subwayMaxDailyDateWeekly,
    'busWeeklyRidership': busWeeklyRidership,
    'busYearlyRidership': busYearlyRidership,
    'busMaxDailyRidershipWeekly': busMaxDailyRidershipWeekly,
    'busMaxDailyDateWeekly': busMaxDailyDateWeekly,
    'subwayMaxAnnualDay': subwayMaxAnnualDay,
    'subwayMaxAnnualDayMeanRidership': subwayMaxAnnualDayMeanRidership,
    'subwayMinAnnualDay': subwayMinAnnualDay,
    'subwayMinAnnualDayMeanRidership': subwayMinAnnualDayMeanRidership,
    'busMaxAnnualDay': busMaxAnnualDay,
    'busMaxAnnualDayMeanRidership': busMaxAnnualDayMeanRidership,
    'busMinAnnualDay': busMinAnnualDay,
    'busMinAnnualDayMeanRidership': busMinAnnualDayMeanRidership,
    'tramWeeklyRidership': tramWeeklyRidership,
    'tramMaxDailyRidershipWeekly': tramMaxDailyRidershipWeekly,
    'tramMaxDailyDateWeekly': tramMaxDailyDateWeekly
}

#print(data)

# Write json
with open('./data/data.json', 'w') as f:
    json.dump(data, f)