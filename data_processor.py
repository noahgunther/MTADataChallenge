'''This script runs once daily at https://gunthern.pythonanywhere.com to retrieve, calculate and cache site data for https://noahgunther.com/mta'''

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib as mpl

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
if (dateMostRecent.hour != 23):
    dateMostRecent = dateMostRecent - timedelta(days=1)
    dateMostRecent = dateMostRecent.replace(hour=23)
dateWeekStart = dateMostRecent - timedelta(days=6, hours=23)
dateYearStart = dateMostRecent - timedelta(days=364, hours=23)

dateMostRecentLong = longDateConstructor(dateMostRecent)
dateWeekStartLong = longDateConstructor(dateWeekStart)
dateYearStartLong = longDateConstructor(dateYearStart)

# Create array of hours in week 
hoursInWeek = []
h = 0
d = 6
for i in range(168):
    t = 'T'
    if h < 10: 
        t = 'T0'
    hoursInWeek.append(str(dateMostRecent - timedelta(days=d))[:10] + t + str(h))
    h += 1
    if h > 23:
        h = 0
        d -= 1

# Create labels for hours in week
hoursInWeekLabels = []
for i in range(len(hoursInWeek)):
    if hoursInWeek[i][11:] == "18":
        hoursInWeekLabels.append('18:00')
    elif hoursInWeek[i][11:] == "12":
        hoursInWeekLabels.append('12:00')
    elif hoursInWeek[i][11:] == "06":
        hoursInWeekLabels.append('6:00')
    elif hoursInWeek[i][11:] == "00":
        d = longDateConstructor(dateDeconstructor(hoursInWeek[i]))[:-6]
        ds = d.split('day, ', 1)[1]
        hoursInWeekLabels.append(d[:3] + ', ' + ds[:3] + '. ' + ds.split(' ', 2)[1] + ', 00:00')
    else:
        hoursInWeekLabels.append('')
    
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
        subwayDaysOfWeekTally[0] += 1
        subwayDaysOfWeekRidership[0] += subwayDailyRidership
        busDaysOfWeekTally[0] += 1
        busDaysOfWeekRidership[0] += busDailyRidership
    elif day == 'Tue':
        subwayDaysOfWeekTally[1] += 1
        subwayDaysOfWeekRidership[1] += subwayDailyRidership
        busDaysOfWeekTally[1] += 1
        busDaysOfWeekRidership[1] += busDailyRidership
    elif day == 'Wed':
        subwayDaysOfWeekTally[2] += 1
        subwayDaysOfWeekRidership[2] += subwayDailyRidership
        busDaysOfWeekTally[2] += 1
        busDaysOfWeekRidership[2] += busDailyRidership
    elif day == 'Thu':
        subwayDaysOfWeekTally[3] += 1
        subwayDaysOfWeekRidership[3] += subwayDailyRidership
        busDaysOfWeekTally[3] += 1
        busDaysOfWeekRidership[3] += busDailyRidership
    elif day == 'Fri':
        subwayDaysOfWeekTally[4] += 1
        subwayDaysOfWeekRidership[4] += subwayDailyRidership
        busDaysOfWeekTally[4] += 1
        busDaysOfWeekRidership[4] += busDailyRidership
    elif day == 'Sat':
        subwayDaysOfWeekTally[5] += 1
        subwayDaysOfWeekRidership[5] += subwayDailyRidership
        busDaysOfWeekTally[5] += 1
        busDaysOfWeekRidership[5] += busDailyRidership
    elif day == 'Sun':
        subwayDaysOfWeekTally[6] += 1
        subwayDaysOfWeekRidership[6] += subwayDailyRidership
        busDaysOfWeekTally[6] += 1
        busDaysOfWeekRidership[6] += busDailyRidership

# Calculate subway yearly data
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

# Calculate bus yearly data
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
url = "https://data.ny.gov/resource/wujg-7c2s.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&transit_mode=tram&$where=transit_timestamp+between%27" + queryDateConstructor(dateWeekStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27&$order=transit_timestamp+DESC&$limit=10000"
data = requests.get(url).json()
tramWeeklyRidership = 0
tramDailyRidership = [0,0,0,0,0,0,0]
tramMaxDailyRidershipWeekly = 0
tramMaxDailyDateWeekly = ''

tramHourlyRidership = []
for h in range(len(hoursInWeek)):
    tramHourlyRidership.append(0)

for d in data:
    tramRidership = int(float(d['ridership']))
    tramWeeklyRidership += tramRidership
    ridershipHour = d['transit_timestamp'][:13]
    
    # Hourly ridership for tram
    for h in range(len(hoursInWeek)):
        if ridershipHour == hoursInWeek[h]:
            tramHourlyRidership[h] += tramRidership

    # Daily ridership for tram
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

# Subway
subwayStationMaxRidershipWeeklyCount = []
subwayStationMaxRidershipWeeklyStation = []
subwayStationMaxRidershipWeeklyBorough = []
subwayHourlyRidership = []
for h in range(len(hoursInWeek)):
    subwayHourlyRidership.append(0)

for i in range(1000):
    stationComplexId = str(i+1)
    url = "https://data.ny.gov/resource/wujg-7c2s.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&station_complex_id=" + stationComplexId + "&$where=transit_timestamp+between+%27" + queryDateConstructor(dateWeekStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27&$order=transit_timestamp+DESC&$limit=10000"
    data = requests.get(url).json()
    if (data != []):
        stationWeeklyRidership = 0
        for d in data:
            ridership = int(float(d['ridership']))
            stationWeeklyRidership += ridership
            ridershipHour = d['transit_timestamp'][:13]

            for h in range(len(hoursInWeek)):
                if ridershipHour == hoursInWeek[h]:
                    subwayHourlyRidership[h] += ridership

        if i == 0:
            subwayStationMaxRidershipWeeklyCount.insert(0, stationWeeklyRidership)
            subwayStationMaxRidershipWeeklyStation.insert(0, data[0]['station_complex'])
            subwayStationMaxRidershipWeeklyBorough.insert(0, data[0]['borough'])

        inserted = False
        for j in range(len(subwayStationMaxRidershipWeeklyCount)):
            if stationWeeklyRidership > subwayStationMaxRidershipWeeklyCount[j]:
                subwayStationMaxRidershipWeeklyCount.insert(j, stationWeeklyRidership)
                subwayStationMaxRidershipWeeklyStation.insert(j, data[0]['station_complex'])
                subwayStationMaxRidershipWeeklyBorough.insert(j, data[0]['borough'])
                inserted = True
                break

        if not inserted:
            subwayStationMaxRidershipWeeklyCount.append(stationWeeklyRidership)
            subwayStationMaxRidershipWeeklyStation.append(data[0]['station_complex'])
            subwayStationMaxRidershipWeeklyBorough.append(data[0]['borough'])

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
    'tramMaxDailyDateWeekly': tramMaxDailyDateWeekly,
    'subwayStationMaxRidershipWeeklyStation': subwayStationMaxRidershipWeeklyStation,
    'subwayStationMaxRidershipWeeklyBorough': subwayStationMaxRidershipWeeklyBorough,
    'subwayStationMaxRidershipWeeklyCount': subwayStationMaxRidershipWeeklyCount
}

#print(data)

# Write json
with open('./data/data.json', 'w') as f:
    json.dump(data, f)

# Create graphs
plt.style.use(['dark_background'])
plt.hsv()
fpathreg = Path("./fonts/Helvetica.ttf")
fpathbold = Path("./fonts/Helvetica-Bold.ttf")
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams["figure.figsize"] = [14.228,14.228]
fig, ax = plt.subplots()

# Hourly tram ridership for the week
plt.xlabel('Time', fontsize=26, font=fpathreg)
plt.ylabel('Ridership', fontsize=26, font=fpathreg)

# Ticks and labels
x = []
for i in range(168):
    x.append(i)
plt.xticks(rotation=35, ticks=x, labels=hoursInWeekLabels, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)
plt.plot(hoursInWeek, tramHourlyRidership, color=[1,1,1,1], linewidth=0.05)
ax.set_ylim(ymin=0)
for n, label in enumerate(ax.xaxis.get_ticklabels()):
    if n % 24 != 0:
        label.set_fontsize(11)
for n, tick in enumerate(ax.xaxis.get_ticklines()):
    if n % 12 != 0:
        tick.set_visible(False)

# Colors and fill
tramMaxWeeklyHour = 0
for h in tramHourlyRidership:
    if h > tramMaxWeeklyHour:
        tramMaxWeeklyHour = h
tramHourlyRidershipSubstep = 10
for i in range(168):
    if i > 0:
        stepXStart = x[i-1]
        stepXEnd = x[i]
        stepYStart = tramHourlyRidership[i-1]
        stepYEnd = tramHourlyRidership[i]
        substepLength = 1 / tramHourlyRidershipSubstep
        for j in range(tramHourlyRidershipSubstep):
            lerp = stepYStart + (stepYEnd - stepYStart) * (substepLength * j)
            HSVcolor = [abs(1.0-(lerp / tramMaxWeeklyHour)) * 0.75, 1.0, 1.0]
            plt.fill_between(
                [stepXStart + substepLength * (j+1), stepXEnd - substepLength * (tramHourlyRidershipSubstep - (j+1) + 1)],
                [stepYStart + (stepYEnd - stepYStart) * (substepLength * (j+1)), lerp],
                color=mpl.colors.hsv_to_rgb(HSVcolor),
                linewidth=1
            )

# Output
plt.tight_layout()
plt.savefig('./mysite/media/weeklytramridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Hourly subway ridership for the week
plt.xlabel('Time', fontsize=26, font=fpathreg)
plt.ylabel('Ridership', fontsize=26, font=fpathreg)

# Ticks and labels
x = []
for i in range(168):
    x.append(i)
plt.xticks(rotation=35, ticks=x, labels=hoursInWeekLabels, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)
plt.plot(hoursInWeek, subwayHourlyRidership, color=[1,1,1,1], linewidth=0.05)
ax.set_ylim(ymin=0)
for n, label in enumerate(ax.xaxis.get_ticklabels()):
    if n % 24 != 0:
        label.set_fontsize(11)
for n, tick in enumerate(ax.xaxis.get_ticklines()):
    if n % 12 != 0:
        tick.set_visible(False)

# Colors and fill
subwayMaxWeeklyHour = 0
for h in subwayHourlyRidership:
    if h > subwayMaxWeeklyHour:
        subwayMaxWeeklyHour = h
subwayHourlyRidershipSubstep = 10
for i in range(168):
    if i > 0:
        stepXStart = x[i-1]
        stepXEnd = x[i]
        stepYStart = subwayHourlyRidership[i-1]
        stepYEnd = subwayHourlyRidership[i]
        substepLength = 1 / subwayHourlyRidershipSubstep
        for j in range(subwayHourlyRidershipSubstep):
            lerp = stepYStart + (stepYEnd - stepYStart) * (substepLength * j)
            HSVcolor = [abs(1.0-(lerp / subwayMaxWeeklyHour)) * 0.75, 1.0, 1.0]
            plt.fill_between(
                [stepXStart + substepLength * (j+1), stepXEnd - substepLength * (subwayHourlyRidershipSubstep - (j+1) + 1)],
                [stepYStart + (stepYEnd - stepYStart) * (substepLength * (j+1)), lerp],
                color=mpl.colors.hsv_to_rgb(HSVcolor),
                linewidth=1
            )

# Output
plt.tight_layout()
plt.savefig('./mysite/media/weeklysubwayridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Top subway station weekly ridership comparison
left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
height = subwayStationMaxRidershipWeeklyCount[:15]
tick_label = []
for i in range(15):
    if len(subwayStationMaxRidershipWeeklyStation[i]) > 27:
        tick_label.append(subwayStationMaxRidershipWeeklyStation[i][:27] + '...')
    else:
        tick_label.append(subwayStationMaxRidershipWeeklyStation[i])

plt.xticks(rotation=35, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)

# Colors and format
HSVcolor = []
for c in subwayStationMaxRidershipWeeklyCount[:15]:
    HSVcolor.append([abs(1.0-(c - subwayStationMaxRidershipWeeklyCount[15])/(subwayStationMaxRidershipWeeklyCount[0] - subwayStationMaxRidershipWeeklyCount[15])) * 0.75, 1.0, 1.0])
plt.bar(left, height, tick_label = tick_label, width = 0.95, color = mpl.colors.hsv_to_rgb(HSVcolor))

# Labels
plt.xlabel('Station Name', font=fpathbold, fontsize=26)
plt.ylabel('Ridership', font=fpathbold, fontsize=26)

# Output
plt.tight_layout()
plt.savefig('./mysite/media/weeklystationcomparison.png', transparent=True, dpi=144.0)