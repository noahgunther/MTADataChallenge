// Todo:
// Data:
// - Figure out what live data is possible to access and include (Today).
// - Get most popular stations / stops 2023 from hourly dataset.
// - Get Roosevelt island tram data 2023 from hourly dataset.
// - Get DMV data for parking spaces? UPDATE CARS PANEL WITH DMV INSTEAD OF MTA INFO
// Data vis:
// - Create dynamic graphs.
// - Create JS for google map embedding for stations / stops.
// CSS:
// - Create CSS for live data (old style LCD cells)
// - Create CSS for map borders
// JS functionality:
// - Add dropdowns arrows for more info / individual sources to panels (e.g. number of individual riders estimated at two trips per rider. source: mta.whatever, links to view raw data)
// - Write script for subway cars / buses / cars / parking spots layout and scroll or animation
// - Write autoscroll button functionality
// - Create JS for "back to top" scroll animation
// - Roosevelt island tram animation script
// Graphics:
// - Create graphics for: Subway header (subway logo), Bus header (bus logo), DMV logo (?), subway cars, buses, motor cars, parking spots, bus line logos
// - Roosevelt island tram graphics
// - Place subway / bus graphics according to popular stations / stops etc
// - Create custom google map style to look like MTA map?

import './style.css'

window.addEventListener("load", init, false);

function init() {

    function dateDeconstructor(date) {
        let year = date.substring(0, 4);
        let month = date.substring(5, 7);
        let day = date.substring (8, 10);
        const dateFromString = new Date(year, parseInt(month) - 1, day);
        const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
        let nth = 'th'
        const dayChar = day.slice(-1);
        const tenToNineteen = day.substring(0, 1) == '1';
        if (!tenToNineteen) {
            if (dayChar == '1') nth = 'st';
            else if (dayChar == '2') nth = 'nd';
            else if (dayChar == '3') nth = 'rd';
        }
        let longDate = weekday[dateFromString.getDay()] + ", " + dateFromString.toLocaleString('default', { month: 'long' }) + " " + dateFromString.getDate() + nth;
        return longDate;
    }

    let combinedWeeklyRidership = 0;
    let dateYearStart = '';
    let dateWeekStart = '';
    let dateMostRecent = '';

    function loadData(mode) {

        // Get daily ridership data from past 365 available days
        const xhttpDaily = new XMLHttpRequest();
        xhttpDaily.onload = function() {
            const response = JSON.parse(this.responseText);
            dateYearStart = dateDeconstructor(response[364].date);
            dateWeekStart = dateDeconstructor(response[6].date);
            dateMostRecent = dateDeconstructor(response[0].date);
            
            // Weekly
            let weeklyRidership = 0;
            let maxDailyRidershipWeekly = 0;
            let maxDailyDateWeekly;
            for (let i=0; i<7; i++) {
                let dailyRidership = 0;
                if (mode == 'subway') dailyRidership = parseInt(response[i].subways_total_estimated_ridership);
                else if (mode == 'bus') dailyRidership = parseInt(response[i].buses_total_estimated_ridersip);

                weeklyRidership += dailyRidership;
                if (dailyRidership > maxDailyRidershipWeekly) {
                    maxDailyRidershipWeekly = dailyRidership;
                    maxDailyDateWeekly = response[i].date;
                }
            }

            // Yearly
            let yearlyRidership = 0;
            let daysOfWeekTally = [0,0,0,0,0,0,0];
            let daysOfWeekRidership = [0,0,0,0,0,0,0];
            for (let i=0; i<response.length; i++) {
                let dailyRidership = 0;
                if (mode == 'subway') dailyRidership = parseInt(response[i].subways_total_estimated_ridership);
                else if (mode == 'bus') dailyRidership = parseInt(response[i].buses_total_estimated_ridersip);
                
                yearlyRidership += dailyRidership;

                let day = dateDeconstructor(response[i].date).substring(0, 3);
                if (day == 'Sun') { daysOfWeekTally[0]++; daysOfWeekRidership[0] += dailyRidership; }
                else if (day == 'Mon') { daysOfWeekTally[1]++; daysOfWeekRidership[1] += dailyRidership; }
                else if (day == 'Tue') { daysOfWeekTally[2]++; daysOfWeekRidership[2] += dailyRidership; }
                else if (day == 'Wed') { daysOfWeekTally[3]++; daysOfWeekRidership[3] += dailyRidership; }
                else if (day == 'Thu') { daysOfWeekTally[4]++; daysOfWeekRidership[4] += dailyRidership; }
                else if (day == 'Fri') { daysOfWeekTally[5]++; daysOfWeekRidership[5] += dailyRidership; }
                else if (day == 'Sat') { daysOfWeekTally[6]++; daysOfWeekRidership[6] += dailyRidership; }
            }

            const weekday = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
            let maxAnnualDay = '';
            let maxAnnualDayRidership = 0;
            let maxAnnualDayTally = 0;
            let maxAnnualDayMeanRidership = 0;
            let minAnnualDay = '';
            let minAnnualDayRidership = 0;
            let minAnnualDayTally = 0;
            let minAnnualDayMeanRidership = 0;
            for (let i=0; i<7; i++) {
                if (daysOfWeekRidership[i] > maxAnnualDayRidership) {
                    maxAnnualDayRidership = daysOfWeekRidership[i];
                    maxAnnualDayTally = daysOfWeekTally[i];
                    maxAnnualDay = weekday[i];
                }
                if (minAnnualDayRidership == 0 || daysOfWeekRidership[i] < minAnnualDayRidership) {
                    minAnnualDayRidership = daysOfWeekRidership[i];
                    minAnnualDayTally = daysOfWeekTally[i];
                    minAnnualDay = weekday[i];
                }
            }
            maxAnnualDayMeanRidership = maxAnnualDayRidership / maxAnnualDayTally;
            minAnnualDayMeanRidership = minAnnualDayRidership / minAnnualDayTally;

            if (mode == 'subway') {
                document.getElementById('weekdaterangesubway').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
                document.getElementById('subwayweeklyridership').innerHTML = weeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                //document.getElementById('subwayweeklyfaretotal').innerHTML = (weeklyRidership * 2.9).toFixed(3).slice(0, -1).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwaymaxdailyridership').innerHTML = maxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwaymaxdailycars').innerHTML = (maxDailyRidershipWeekly / 200).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                maxDailyDateWeekly = dateDeconstructor(maxDailyDateWeekly);
                document.getElementById('subwaymaxdailydate0').innerHTML = maxDailyDateWeekly;
                document.getElementById('subwaymaxdailydate1').innerHTML = maxDailyDateWeekly;

                document.getElementById('subwaymaxannualday').innerHTML = maxAnnualDay;
                document.getElementById('subwaymaxannualdaymean').innerHTML = maxAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwayminannualday').innerHTML = minAnnualDay;
                document.getElementById('subwayminannualdaymean').innerHTML = minAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwayyearlyridership').innerHTML = yearlyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwaydailyridershipavg').innerHTML = (yearlyRidership / 365.0).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
            else if (mode == 'bus') {
                document.getElementById('weekdaterangebus').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
                document.getElementById('busweeklyridership').innerHTML = weeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                //document.getElementById('busweeklyfaretotal').innerHTML = (weeklyRidership * 2.9).toFixed(3).slice(0, -1).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busmaxdailyridership').innerHTML = maxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busmaxdailybuses').innerHTML = (maxDailyRidershipWeekly / 200).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                maxDailyDateWeekly = dateDeconstructor(maxDailyDateWeekly);
                document.getElementById('busmaxdailydate0').innerHTML = maxDailyDateWeekly;
                document.getElementById('busmaxdailydate1').innerHTML = maxDailyDateWeekly;
                
                document.getElementById('busmaxannualday').innerHTML = maxAnnualDay;
                document.getElementById('busmaxannualdaymean').innerHTML = maxAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busminannualday').innerHTML = minAnnualDay;
                document.getElementById('busminannualdaymean').innerHTML = minAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busyearlyridership').innerHTML = yearlyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busdailyridershipavg').innerHTML = (yearlyRidership / 365.0).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
            
            document.getElementById('yeardaterange').innerHTML = dateYearStart + ' - ' + dateMostRecent;
            combinedWeeklyRidership += weeklyRidership;
            document.getElementById('totalweeklytransitrides').innerHTML = combinedWeeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }

        xhttpDaily.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$limit=365&$order=date+DESC");
        xhttpDaily.send();
    }

    loadData('subway');
    loadData('bus');

    const tileColors = ['123', '456', '7', 'ACE', 'BDFM', 'G', 'JZ', 'L', 'NQRW', 'S'];
    const tileDivs = document.getElementsByClassName('tilediv');
    const tileCol = tileColors[Math.floor(Math.random() * tileColors.length)];
    for (let i=0; i<tileDivs.length; i++) {
        tileDivs[i].style = 'background-image: url(./media/tile' + tileCol + '.png);'
    }
}