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

# Get most recent available date from all three datasets
datasetTimeQuery = []
timestamps = []
# Get most recent available daily set date
datasetTimeQuery.append("https://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$order=date+DESC&$limit=1")
# Get most recent available hourly subway/tram set date
datasetTimeQuery.append("https://data.ny.gov/resource/5wq4-mkjj.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$order=transit_timestamp+DESC&$limit=1")
# Get most recent available hourly bus set date
datasetTimeQuery.append("https://data.ny.gov/resource/gxb3-akrn.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$order=transit_timestamp+DESC&$limit=1")
for i in range(len(datasetTimeQuery)):
    data = requests.get(datasetTimeQuery[i]).json()
    if i == 0:
        timestamps.append(data[0]['date'])
    else:
        timestamps.append(data[0]['transit_timestamp'])
timestamps.sort()

dateMostRecent = dateDeconstructor(timestamps[0])
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
    if daysInYear[i][8:11] == '01':
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
url = "https://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$limit=365&$order=date+DESC&$where=date+between+%27" + queryDateConstructor(dateYearStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27"
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
url = "https://data.ny.gov/resource/5wq4-mkjj.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&transit_mode=tram&$where=transit_timestamp+between%27" + queryDateConstructor(dateWeekStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27&$order=transit_timestamp+DESC&$limit=10000"
data = requests.get(url).json()
tramWeeklyRidership = 0.0
tramDailyRidership = [0,0,0,0,0,0,0]
tramMaxDailyRidershipWeekly = 0
tramMaxDailyDateWeekly = ''

tramHourlyRidership = []
for h in range(len(hoursInWeek)):
    tramHourlyRidership.append(0.0)

for d in data:
    tramRidership = float(d['ridership'])
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

for h in tramHourlyRidership:
    h = int(h)

# Subway
subwayStationMaxRidershipWeeklyCount = []
subwayStationMaxRidershipWeeklyStation = []
subwayStationMaxRidershipWeeklyBorough = []
subwayHourlyRidership = []
for h in range(len(hoursInWeek)):
    subwayHourlyRidership.append(0.0)

for i in range(636):
    stationComplexId = str(i+1)
    url = "https://data.ny.gov/resource/5wq4-mkjj.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&station_complex_id=" + stationComplexId + "&$where=transit_timestamp+between+%27" + queryDateConstructor(dateWeekStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27&$order=transit_timestamp+DESC&$limit=10000"
    data = requests.get(url).json()
    if (data != []):
        stationWeeklyRidership = 0.0
        for d in data:
            ridership = float(d['ridership'])
            stationWeeklyRidership += ridership
            ridershipHour = d['transit_timestamp'][:13]

            for h in range(len(hoursInWeek)):
                if ridershipHour == hoursInWeek[h]:
                    subwayHourlyRidership[h] += ridership

        if len(subwayStationMaxRidershipWeeklyCount) == 0:
            subwayStationMaxRidershipWeeklyCount.append(int(stationWeeklyRidership))
            subwayStationMaxRidershipWeeklyStation.append(data[0]['station_complex'])
            subwayStationMaxRidershipWeeklyBorough.append(data[0]['borough'])

        else:
            inserted = False
            for j in range(len(subwayStationMaxRidershipWeeklyCount)):
                if stationWeeklyRidership > subwayStationMaxRidershipWeeklyCount[j]:
                    subwayStationMaxRidershipWeeklyCount.insert(j, int(stationWeeklyRidership))
                    subwayStationMaxRidershipWeeklyStation.insert(j, data[0]['station_complex'])
                    subwayStationMaxRidershipWeeklyBorough.insert(j, data[0]['borough'])
                    inserted = True
                    break

            if not inserted:
                subwayStationMaxRidershipWeeklyCount.append(int(stationWeeklyRidership))
                subwayStationMaxRidershipWeeklyStation.append(data[0]['station_complex'])
                subwayStationMaxRidershipWeeklyBorough.append(data[0]['borough'])

for h in subwayHourlyRidership:
    h = int(h)

# Bus
busRouteMaxRidershipWeeklyCount = []
busRouteMaxRidershipWeeklyRoute = []
busRouteMaxRidershipWeeklyBorough = []
busHourlyRidership = []
for h in range(len(hoursInWeek)):
    busHourlyRidership.append(0.0)

busRoute = ['B1', 'B2', 'B3', 'B4', 'B6', 'B7', 'B8', 'B9', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17', 'B20', 'B24', 'B25', 'B26', 'B31', 'B32', 'B35', 'B36', 'B37', 'B38', 'B39', 'B41', 'B42', 'B43', 'B44', 'B44-SBS', 'B45', 'B46', 'B46-SBS', 'B47', 'B48', 'B49', 'B52', 'B54', 'B57', 'B60', 'B61', 'B62', 'B63', 'B64', 'B65', 'B67', 'B68', 'B69', 'B70', 'B74', 'B82', 'B82-SBS', 'B83', 'B84', 'B90', 'B93', 'B94', 'B96', 'B98', 'B99', 'B100', 'B101', 'B103', 'BM1', 'BM2', 'BM3', 'BM4', 'BM5', 'BX92', 'Bx1', 'Bx2', 'Bx3', 'Bx4', 'Bx4A', 'Bx5', 'Bx6', 'Bx6-SBS', 'Bx7', 'Bx8', 'Bx9', 'Bx10', 'Bx11', 'Bx12', 'Bx12-SBS', 'Bx13', 'Bx15', 'Bx16', 'Bx17', 'Bx18A', 'Bx18B', 'Bx19', 'Bx20', 'Bx21', 'Bx22', 'Bx23', 'Bx24', 'Bx25', 'Bx26', 'Bx27', 'Bx28', 'Bx29', 'Bx30', 'Bx31', 'Bx32', 'Bx33', 'Bx34', 'Bx35', 'Bx36', 'Bx38', 'Bx39', 'Bx40', 'Bx41', 'Bx41-SBS', 'Bx42', 'Bx46', 'Bx90', 'BxM1', 'BxM2', 'BxM3', 'BxM4', 'BxM6', 'BxM7', 'BxM8', 'BxM9', 'BxM10', 'BxM11', 'BxM18', 'D90', 'J90', 'L90', 'L91', 'L92', 'M1', 'M2', 'M3', 'M4', 'M5', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12', 'M14A-SBS', 'M14D-SBS', 'M15', 'M15-SBS', 'M20', 'M21', 'M22', 'M23-SBS', 'M31', 'M34-SBS', 'M34A-SBS', 'M35', 'M42', 'M50', 'M55', 'M57', 'M60-SBS', 'M66', 'M72', 'M79-SBS', 'M86-SBS', 'M90', 'M96', 'M98', 'M100', 'M101', 'M102', 'M103', 'M104', 'M106', 'M116', 'M125', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q15', 'Q15A', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20A', 'Q20B', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29', 'Q30', 'Q31', 'Q32', 'Q33', 'Q34', 'Q35', 'Q36', 'Q37', 'Q38', 'Q39', 'Q40', 'Q41', 'Q42', 'Q43', 'Q44-SBS', 'Q46', 'Q47', 'Q48', 'Q49', 'Q50', 'Q52-SBS', 'Q53-SBS', 'Q54', 'Q55', 'Q56', 'Q58', 'Q59', 'Q60', 'Q64', 'Q65', 'Q66', 'Q67', 'Q69', 'Q70-SBS', 'Q72', 'Q76', 'Q77', 'Q83', 'Q84', 'Q85', 'Q88', 'Q90', 'Q92', 'Q93', 'Q96', 'Q100', 'Q101', 'Q102', 'Q103', 'Q104', 'Q107', 'Q108', 'Q110', 'Q111', 'Q112', 'Q113', 'Q114', 'QM1', 'QM2', 'QM3', 'QM4', 'QM5', 'QM6', 'QM7', 'QM8', 'QM10', 'QM11', 'QM12', 'QM15', 'QM16', 'QM17', 'QM18', 'QM20', 'QM21', 'QM24', 'QM25', 'QM31', 'QM32', 'QM34', 'QM35', 'QM36', 'QM40', 'QM42', 'QM44', 'S40', 'S42', 'S44', 'S46', 'S48', 'S51', 'S52', 'S53', 'S54', 'S55', 'S56', 'S57', 'S59', 'S61', 'S62', 'S66', 'S74', 'S76', 'S78', 'S79-SBS', 'S81', 'S84', 'S86', 'S89', 'S90', 'S91', 'S92', 'S93', 'S94', 'S96', 'S98', 'SIM1', 'SIM1C', 'SIM2', 'SIM3', 'SIM3C', 'SIM4', 'SIM4C', 'SIM4X', 'SIM5', 'SIM6', 'SIM7', 'SIM8', 'SIM8X', 'SIM9', 'SIM10', 'SIM11', 'SIM15', 'SIM22', 'SIM23', 'SIM24', 'SIM25', 'SIM26', 'SIM30', 'SIM31', 'SIM32', 'SIM33', 'SIM33C', 'SIM34', 'SIM35', 'X27', 'X28', 'X37', 'X38', 'X63', 'X64', 'X68']
for i in range(len(busRoute)):
    route = busRoute[i].upper()
    if route[-3:] == 'SBS':
        route = route.split('-')[0] + '%2B'
    borough = ''
    if route[:1] == 'B':
        borough = 'Brooklyn'
        if route[:2] == 'BM':
            borough = 'Brooklyn - Manhattan Express'
        elif route[:2] == 'BX':
            borough = 'Bronx'
            if route[:3] == 'BXM':
                borough = 'Bronx - Manhattan Express'
    elif route[:1] == 'M':
        borough = 'Manhattan'
    elif route[:1] == 'Q':
        borough = 'Queens'
        if route[:2] == 'QM':
            borough = 'Queens - Manhattan Express'
    elif route[:1] == 'S':
        borough = 'Staten Island'
        if route[:3] == 'SIM':
            borough = 'Staten Island - Manhattan Express'
    elif route[:1] == 'X':
        borough = 'Brooklyn/Queens - Midtown Manhattan Express'
    elif route[:1] == 'D':
        borough = 'D Train Shuttle Bus'
    elif route[:1] == 'J':
        borough = 'J Train Shuttle Bus'
    elif route[:1] == 'L':
        borough = 'L Train Shuttle Bus'
    url = "https://data.ny.gov/resource/gxb3-akrn.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&bus_route=" + route + "&$where=transit_timestamp+between+%27" + queryDateConstructor(dateWeekStart) + "%27+and+%27" + queryDateConstructor(dateMostRecent) + "%27&$order=transit_timestamp+DESC&$limit=10000"
        
    data = requests.get(url).json()
    if (data != []):
        routeWeeklyRidership = 0.0
        for d in data:
            ridership = float(d['ridership'])
            routeWeeklyRidership += ridership
            ridershipHour = d['transit_timestamp'][:13]

            for h in range(len(hoursInWeek)):
                if ridershipHour == hoursInWeek[h]:
                    busHourlyRidership[h] += ridership

        if len(busRouteMaxRidershipWeeklyCount) == 0:
            busRouteMaxRidershipWeeklyCount.append(int(routeWeeklyRidership))
            busRouteMaxRidershipWeeklyRoute.append(busRoute[i])
            busRouteMaxRidershipWeeklyBorough.append(borough)

        else:
            inserted = False
            for j in range(len(busRouteMaxRidershipWeeklyCount)):
                if routeWeeklyRidership > busRouteMaxRidershipWeeklyCount[j]:
                    busRouteMaxRidershipWeeklyCount.insert(j, int(routeWeeklyRidership))
                    busRouteMaxRidershipWeeklyRoute.insert(j, busRoute[i])
                    busRouteMaxRidershipWeeklyBorough.insert(j, borough)
                    inserted = True
                    break

            if not inserted:
                busRouteMaxRidershipWeeklyCount.append(int(routeWeeklyRidership))
                busRouteMaxRidershipWeeklyRoute.append(busRoute[i])
                busRouteMaxRidershipWeeklyBorough.append(borough)

for h in busHourlyRidership:
    h = int(h)

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
    'subwayMaxAnnualDay': subwayMaxAnnualDay,
    'subwayMaxMeanDayRidership': subwayMaxMeanDayRidership,
    'subwayMinAnnualDay': subwayMinAnnualDay,
    'subwayMinMeanDayRidership': subwayMinMeanDayRidership,
    'subwayStationMaxRidershipWeeklyStation': subwayStationMaxRidershipWeeklyStation,
    'subwayStationMaxRidershipWeeklyBorough': subwayStationMaxRidershipWeeklyBorough,
    'subwayStationMaxRidershipWeeklyCount': subwayStationMaxRidershipWeeklyCount,
    'busWeeklyRidership': busWeeklyRidership,
    'busYearlyRidership': busYearlyRidership,
    'busMaxAnnualDateRidership': busMaxAnnualDateRidership,
    'busMaxAnnualDate': busMaxAnnualDate,
    'busMinAnnualDateRidership': busMinAnnualDateRidership,
    'busMinAnnualDate': busMinAnnualDate,
    'busMaxDailyRidershipWeekly': busMaxDailyRidershipWeekly,
    'busMaxDailyDateWeekly': busMaxDailyDateWeekly,
    'busMaxAnnualDay': busMaxAnnualDay,
    'busMaxMeanDayRidership': busMaxMeanDayRidership,
    'busMinAnnualDay': busMinAnnualDay,
    'busMinMeanDayRidership': busMinMeanDayRidership,
    'busRouteMaxRidershipWeeklyRoute': busRouteMaxRidershipWeeklyRoute,
    'busRouteMaxRidershipWeeklyBorough': busRouteMaxRidershipWeeklyBorough,
    'busRouteMaxRidershipWeeklyCount': busRouteMaxRidershipWeeklyCount,
    'tramWeeklyRidership': int(tramWeeklyRidership),
    'tramMaxDailyRidershipWeekly': tramMaxDailyRidershipWeekly,
    'tramMaxDailyDateWeekly': tramMaxDailyDateWeekly
}

#print(data)

# Write json
with open('./data.json', 'w') as f:
    json.dump(data, f)

# Create graphs
plt.style.use(['dark_background'])
plt.hsv()
fpathreg = Path("./fonts/Helvetica.ttf")
fpathbold = Path("./fonts/Helvetica-Bold.ttf")
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams["figure.figsize"] = [14.228, 9.49]
fig, ax = plt.subplots()

# Hourly tram ridership for the week
plt.xlabel('Time (week)', fontsize=26, font=fpathreg)
plt.ylabel('Ridership (hourly)', fontsize=26, font=fpathreg)

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
plt.savefig('./media/weeklytramridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Hourly subway ridership for the week
plt.xlabel('Time (week)', fontsize=26, font=fpathreg)
plt.ylabel('Ridership (hourly)', fontsize=26, font=fpathreg)

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
plt.savefig('./media/weeklysubwayridership.png', transparent=True, dpi=144.0)

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
plt.ylabel('Ridership (week)', font=fpathbold, fontsize=26)

# Output
plt.tight_layout()
plt.savefig('./media/weeklystationcomparison.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Hourly bus ridership for the week
plt.xlabel('Time (week)', fontsize=26, font=fpathreg)
plt.ylabel('Ridership (hourly)', fontsize=26, font=fpathreg)

# Ticks and labels
x = []
for i in range(168):
    x.append(i)
plt.xticks(rotation=35, ticks=x, labels=hoursInWeekLabels, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)
plt.plot(hoursInWeek, busHourlyRidership, color=[1,1,1,1], linewidth=0.05)
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
busMaxWeeklyHour = 0
for h in busHourlyRidership:
    if h > busMaxWeeklyHour:
        busMaxWeeklyHour = h
busHourlyRidershipSubstep = 10
for i in range(168):
    if i > 0:
        stepXStart = x[i-1]
        stepXEnd = x[i]
        stepYStart = busHourlyRidership[i-1]
        stepYEnd = busHourlyRidership[i]
        substepLength = 1 / busHourlyRidershipSubstep
        for j in range(busHourlyRidershipSubstep):
            lerp = stepYStart + (stepYEnd - stepYStart) * (substepLength * j)
            HSVcolor = [abs(1.0-(lerp / busMaxWeeklyHour)) * 0.75, 1.0, 1.0]
            plt.fill_between(
                [stepXStart + substepLength * (j+1), stepXEnd - substepLength * (busHourlyRidershipSubstep - (j+1) + 1)],
                [stepYStart + (stepYEnd - stepYStart) * (substepLength * (j+1)), lerp],
                color=mpl.colors.hsv_to_rgb(HSVcolor),
                linewidth=1
            )

# Output
plt.tight_layout()
plt.savefig('./media/weeklybusridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Top bus route weekly ridership comparison
left = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
height = busRouteMaxRidershipWeeklyCount[:15]
tick_label = []
for i in range(15):
    tick_label.append(busRouteMaxRidershipWeeklyRoute[i] + " (" + busRouteMaxRidershipWeeklyBorough[i] + ")")

plt.xticks(rotation=35, ha='right', font=fpathreg, fontsize=16)
plt.yticks(font=fpathreg, fontsize=18)
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# Colors and format
HSVcolor = []
for c in busRouteMaxRidershipWeeklyCount[:15]:
    HSVcolor.append([abs(1.0-(c - busRouteMaxRidershipWeeklyCount[15])/(busRouteMaxRidershipWeeklyCount[0] - busRouteMaxRidershipWeeklyCount[15])) * 0.75, 1.0, 1.0])
plt.bar(left, height, tick_label = tick_label, width = 0.95, color = mpl.colors.hsv_to_rgb(HSVcolor))

# Labels
plt.xlabel('Bus Route', font=fpathbold, fontsize=26)
plt.ylabel('Ridership (week)', font=fpathbold, fontsize=26)

# Output
plt.tight_layout()
plt.savefig('./media/weeklyroutecomparison.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Daily subway ridership for the year
plt.xlabel('Time (year)', fontsize=26, font=fpathreg)
plt.ylabel('Ridership (daily)', fontsize=26, font=fpathreg)

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
plt.savefig('./media/yearlysubwayridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Daily bus ridership for the year
plt.xlabel('Time (year)', fontsize=26, font=fpathreg)
plt.ylabel('Ridership (daily)', fontsize=26, font=fpathreg)

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
plt.savefig('./media/yearlybusridership.png', transparent=True, dpi=144.0)

plt.clf()
fig, ax = plt.subplots()

# Subway & bus day of week comparison for the year
plt.xticks(font=fpathreg, fontsize=18)
plt.yticks(font=fpathreg, fontsize=16)
ax.get_yaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# Colors and format
plt.bar(weekday, subwayMeanDayRidership, width=-0.4, align='edge', color=[0, 0.223, 0.651, 1])
plt.bar(weekday, busMeanDayRidership, width=0.4, align='edge', color=[0.5, 0.5, 0.52, 1])

# Labels
plt.ylabel('Mean ridership (year)', font=fpathbold, fontsize=26)

# Legend
subway_patch = mpl.patches.Patch(color=[0, 0.223, 0.651, 1], label='Subway (left)')
bus_patch = mpl.patches.Patch(color=[0.5, 0.5, 0.52, 1], label='Bus (right)') 
plt.legend(handles=[subway_patch, bus_patch], prop={'size': 15, 'family': 'monospace', 'style': 'oblique'})

# Output
plt.tight_layout()
plt.savefig('./media/meandayofweekcomparison.png', transparent=True, dpi=144.0)