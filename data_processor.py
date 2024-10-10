'''This script runs once daily at https://gunthern.pythonanywhere.com to retrieve, calculate and cache site data for https://noahgunther.com/mta'''

import requests
import json
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib as mpl

weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
month = ["January","February","March","April","May","June","July","August","September","October","November","December"]

def dateDeconstructor(dateString):
    year = int(dateString[:4])
    mo = int(dateString[5:7])
    day = int(dateString[8:10])
    hour = int(dateString[11:13])
    return datetime(year, mo, day, hour, 0, 0, 0)

def longDateConstructor(date):
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

# Create array of days in year 
daysInYear = []
d = 364
for i in range(365):
    daysInYear.append(str(dateMostRecent - timedelta(days=d))[:10])
    d -= 1

# Create labels for hours in week
daysInYearLabels = []
for i in range(len(daysInYear)):
    if i == 0 or i == len(daysInYear)-1:
        daysInYearLabels.append(month[int(daysInYear[i][5:7])-1] + " " + daysInYear[i][8:11] + ", " + daysInYear[i][:4])
    elif daysInYear[i][8:11] == '01':
        daysInYearLabels.append(month[int(daysInYear[i][5:7])-1] + " 01, " + daysInYear[i][:4])
    else:
        daysInYearLabels.append('')

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
    subwayRidership = int(data[i]['subways_total_estimated_ridership'])
    busRidership = int(data[i]['buses_total_estimated_ridersip'])

    subwayWeeklyRidership += subwayRidership
    if (subwayRidership > subwayMaxDailyRidershipWeekly):
        subwayMaxDailyRidershipWeekly = subwayRidership
        subwayMaxDailyDateWeekly = longDateConstructor(dateDeconstructor(data[i]['date']))

    busWeeklyRidership += busRidership
    if (busRidership > busMaxDailyRidershipWeekly):
        busMaxDailyRidershipWeekly = busRidership
        busMaxDailyDateWeekly = longDateConstructor(dateDeconstructor(data[i]['date']))

# Latest year of ridership from daily data
subwayYearlyRidership = 0
subwayDailyRidership = []
for i in range(365):
    subwayDailyRidership.append(0)
subwayDaysOfWeekTally = [0,0,0,0,0,0,0]
subwayDaysOfWeekRidership = [0,0,0,0,0,0,0]
subwayMaxAnnualDateRidership = 0
subwayMaxAnnualDate = ''
subwayMinAnnualDateRidership = 0
subwayMinAnnualDate = ''
busYearlyRidership = 0
busDailyRidership = []
for i in range(365):
    busDailyRidership.append(0)
busDaysOfWeekTally = [0,0,0,0,0,0,0]
busDaysOfWeekRidership = [0,0,0,0,0,0,0]
busMaxAnnualDateRidership = 0
busMaxAnnualDate = ''
busMinAnnualDateRidership = 0
busMinAnnualDate = ''
for d in data:
    day = longDateConstructor(dateDeconstructor(d['date']))

    subwayRidership = int(d['subways_total_estimated_ridership'])
    busRidership = int(d['buses_total_estimated_ridersip'])

    # Daily ridership for subway / bus
    for t in range(len(daysInYear)):
           if d['date'][:10] == daysInYear[t]:
            subwayDailyRidership[t] += subwayRidership
            busDailyRidership[t] += busRidership

    if subwayRidership > subwayMaxAnnualDateRidership:
        subwayMaxAnnualDateRidership = subwayRidership
        subwayMaxAnnualDate = day
    if subwayRidership < subwayMinAnnualDateRidership or subwayMinAnnualDateRidership == 0:
        subwayMinAnnualDateRidership = subwayRidership
        subwayMinAnnualDate = day

    if busRidership > busMaxAnnualDateRidership:
        busMaxAnnualDateRidership = busRidership
        busMaxAnnualDate = day
    if busRidership < busMinAnnualDateRidership or busMinAnnualDateRidership == 0:
        busMinAnnualDateRidership = busRidership
        busMinAnnualDate = day

    subwayYearlyRidership += subwayRidership
    busYearlyRidership += busRidership

    if day[:3] == 'Mon':
        subwayDaysOfWeekTally[0] += 1
        subwayDaysOfWeekRidership[0] += subwayRidership
        busDaysOfWeekTally[0] += 1
        busDaysOfWeekRidership[0] += busRidership
    elif day[:3] == 'Tue':
        subwayDaysOfWeekTally[1] += 1
        subwayDaysOfWeekRidership[1] += subwayRidership
        busDaysOfWeekTally[1] += 1
        busDaysOfWeekRidership[1] += busRidership
    elif day[:3] == 'Wed':
        subwayDaysOfWeekTally[2] += 1
        subwayDaysOfWeekRidership[2] += subwayRidership
        busDaysOfWeekTally[2] += 1
        busDaysOfWeekRidership[2] += busRidership
    elif day[:3] == 'Thu':
        subwayDaysOfWeekTally[3] += 1
        subwayDaysOfWeekRidership[3] += subwayRidership
        busDaysOfWeekTally[3] += 1
        busDaysOfWeekRidership[3] += busRidership
    elif day[:3] == 'Fri':
        subwayDaysOfWeekTally[4] += 1
        subwayDaysOfWeekRidership[4] += subwayRidership
        busDaysOfWeekTally[4] += 1
        busDaysOfWeekRidership[4] += busRidership
    elif day[:3] == 'Sat':
        subwayDaysOfWeekTally[5] += 1
        subwayDaysOfWeekRidership[5] += subwayRidership
        busDaysOfWeekTally[5] += 1
        busDaysOfWeekRidership[5] += busRidership
    elif day[:3] == 'Sun':
        subwayDaysOfWeekTally[6] += 1
        subwayDaysOfWeekRidership[6] += subwayRidership
        busDaysOfWeekTally[6] += 1
        busDaysOfWeekRidership[6] += busRidership

# Calculate subway yearly data
subwayMeanDayRidership = [0,0,0,0,0,0,0]
subwayMaxAnnualDay = ''
subwayMaxMeanDayRidership = 0
subwayMinAnnualDay = ''
subwayMinMeanDayRidership = 0

for i in range(7):
    subwayMeanDayRidership[i] = subwayDaysOfWeekRidership[i] / subwayDaysOfWeekTally[i]

    if subwayMeanDayRidership[i] > subwayMaxMeanDayRidership:
        subwayMaxMeanDayRidership = subwayMeanDayRidership[i]
        subwayMaxAnnualDay = weekday[i]

    if i == 0 or subwayMeanDayRidership[i] < subwayMinMeanDayRidership:
        subwayMinMeanDayRidership = subwayMeanDayRidership[i]
        subwayMinAnnualDay = weekday[i]

# Calculate bus yearly data
busMeanDayRidership = [0,0,0,0,0,0,0]
busMaxAnnualDay = ''
busMaxMeanDayRidership = 0
busMinAnnualDay = ''
busMinMeanDayRidership = 0

for i in range(7):
    busMeanDayRidership[i] = busDaysOfWeekRidership[i] / busDaysOfWeekTally[i]

    if busMeanDayRidership[i] > busMaxMeanDayRidership:
        busMaxMeanDayRidership = busMeanDayRidership[i]
        busMaxAnnualDay = weekday[i]

    if i == 0 or busMeanDayRidership[i] < busMinMeanDayRidership:
        busMinMeanDayRidership = busMeanDayRidership[i]
        busMinAnnualDay = weekday[i]

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
    'subwayMaxAnnualDateRidership': subwayMaxAnnualDateRidership,
    'subwayMaxAnnualDate': subwayMaxAnnualDate,
    'subwayMinAnnualDateRidership': subwayMinAnnualDateRidership,
    'subwayMinAnnualDate': subwayMinAnnualDate,
    'subwayMaxDailyRidershipWeekly': subwayMaxDailyRidershipWeekly,
    'subwayMaxDailyDateWeekly': subwayMaxDailyDateWeekly,
    'busWeeklyRidership': busWeeklyRidership,
    'busYearlyRidership': busYearlyRidership,
    'busMaxAnnualDateRidership': busMaxAnnualDateRidership,
    'busMaxAnnualDate': busMaxAnnualDate,
    'busMinAnnualDateRidership': busMinAnnualDateRidership,
    'busMinAnnualDate': busMinAnnualDate,
    'busMaxDailyRidershipWeekly': busMaxDailyRidershipWeekly,
    'busMaxDailyDateWeekly': busMaxDailyDateWeekly,
    'subwayMaxAnnualDay': subwayMaxAnnualDay,
    'subwayMaxMeanDayRidership': subwayMaxMeanDayRidership,
    'subwayMinAnnualDay': subwayMinAnnualDay,
    'subwayMinMeanDayRidership': subwayMinMeanDayRidership,
    'busMaxAnnualDay': busMaxAnnualDay,
    'busMaxMeanDayRidership': busMaxMeanDayRidership,
    'busMinAnnualDay': busMinAnnualDay,
    'busMinMeanDayRidership': busMinMeanDayRidership,
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
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
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
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
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
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

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

plt.clf()
fig, ax = plt.subplots()

# Daily subway ridership for the year
plt.xlabel('Time', fontsize=26, font=fpathreg)
plt.ylabel('Ridership', fontsize=26, font=fpathreg)

# Ticks and labels
x = []
for i in range(365):
    x.append(i)
plt.xticks(rotation=35, ticks=x, labels=daysInYearLabels, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)
plt.plot(daysInYear, subwayDailyRidership, color=[1,1,1,1], linewidth=0.05)
ax.set_ylim(ymin=0)
plt.ticklabel_format(axis='y', style='plain')
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
for n, tick in enumerate(ax.xaxis.get_ticklines()):
    if n % 2 != 0:
        tick.set_visible(False)
    elif daysInYearLabels[int(n / 2)] == '':
        tick.set_visible(False)

# Colors and fill
subwayDailyRidershipSubstep = 10
for i in range(365):
    if i > 0:
        stepXStart = x[i-1]
        stepXEnd = x[i]
        stepYStart = subwayDailyRidership[i-1]
        stepYEnd = subwayDailyRidership[i]
        substepLength = 1 / subwayDailyRidershipSubstep
        for j in range(subwayDailyRidershipSubstep):
            lerp = stepYStart + (stepYEnd - stepYStart) * (substepLength * j)
            HSVcolor = [abs(1.0-(lerp / subwayMaxAnnualDateRidership)) * 0.75, 1.0, 1.0]
            plt.fill_between(
                [stepXStart + substepLength * (j+1), stepXEnd - substepLength * (subwayDailyRidershipSubstep - (j+1) + 1)],
                [stepYStart + (stepYEnd - stepYStart) * (substepLength * (j+1)), lerp],
                color=mpl.colors.hsv_to_rgb(HSVcolor),
                linewidth=1
            )

# Output
plt.tight_layout()
plt.savefig('./mysite/media/yearlysubwayridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Daily bus ridership for the year
plt.xlabel('Time', fontsize=26, font=fpathreg)
plt.ylabel('Ridership', fontsize=26, font=fpathreg)

# Ticks and labels
x = []
for i in range(365):
    x.append(i)
plt.xticks(rotation=35, ticks=x, labels=daysInYearLabels, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)
plt.plot(daysInYear, busDailyRidership, color=[1,1,1,1], linewidth=0.05)
ax.set_ylim(ymin=0)
plt.ticklabel_format(axis='y', style='plain')
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
for n, tick in enumerate(ax.xaxis.get_ticklines()):
    if n % 2 != 0:
        tick.set_visible(False)
    elif daysInYearLabels[int(n / 2)] == '':
        tick.set_visible(False)

# Colors and fill
busDailyRidershipSubstep = 10
for i in range(365):
    if i > 0:
        stepXStart = x[i-1]
        stepXEnd = x[i]
        stepYStart = busDailyRidership[i-1]
        stepYEnd = busDailyRidership[i]
        substepLength = 1 / busDailyRidershipSubstep
        for j in range(busDailyRidershipSubstep):
            lerp = stepYStart + (stepYEnd - stepYStart) * (substepLength * j)
            HSVcolor = [abs(1.0-(lerp / busMaxAnnualDateRidership)) * 0.75, 1.0, 1.0]
            plt.fill_between(
                [stepXStart + substepLength * (j+1), stepXEnd - substepLength * (busDailyRidershipSubstep - (j+1) + 1)],
                [stepYStart + (stepYEnd - stepYStart) * (substepLength * (j+1)), lerp],
                color=mpl.colors.hsv_to_rgb(HSVcolor),
                linewidth=1
            )

# Output
plt.tight_layout()
plt.savefig('./mysite/media/yearlybusridership.png', transparent=True, dpi=144.0)