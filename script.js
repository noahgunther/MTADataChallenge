// Todo:
// Data:
// - Figure out what live data is possible to access and include.
// - Get the rest of the data needed from MTA datasets.
// - Calculate fare data based on hourly dataset and fare amounts
// - Get most popular stations and lines servicing those stations
// - Get DMV data for parking spaces? UPDATE CARS PANEL WITH DMV INSTEAD OF MTA INFO
// - Add data for most popular stops in each borough?
// - Roosevelt island tram?
// Data vis:
// - Add some graphs for activity by borough or that kind of thing.
// - Create JS for google map embedding for station.
// CSS:
// - Create CSS for live data (old style LCD cells)
// - Create CSS for map borders
// JS functionality:
// - Tile divider color(s) based on most popular subway station lines
// - Add dropdowns arrows for more info / individual sources to panels (e.g. number of individual riders estimated at two trips per rider. source: mta.whatever, links to view raw data)
// - Write script for subway cars / buses / cars / parking spots layout and scroll or animation
// - Write autoscroll button functionality
// - Create JS for "back to top" scroll animation
// - Roosevelt island tram animation script
// Graphics:
// - Create graphics for: Subway header (subway logo), Bus header (bus logo), DMV logo (?), subway cars, buses, motor cars, parking spots, subway line logos, bus line logos, general MTA seasoning
// - Roosevelt island tram graphics

import './style.css'

window.addEventListener("load", init, false);

function init() {

    /*function dateConstructor(subStart, range) {
        const dates = [];
        for (let i=0; i<range; i++) {
            const date = new Date();
            date.setDate(date.getDate() - subStart);
            let day = date.getDate().toString();
            day.length < 2 ? day = '0' + day : day;
            let month = (date.getMonth() + 1).toString();
            month.length < 2 ? month = '0' + month : month;
            let year = date.getFullYear();
            dates.push(year + "-" + month + "-" + day);
            subStart++;
        }
        return dates;
    }*/

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

    let test = 0;

    function loadData(element) {
        /*let dateString = '';
        for (let i=0; i<dates.length; i++) {
            dateString += "date='" + dates[i];
            if (i != dates.length-1) {
                dateString += "' OR ";
            }
            else {
                dateString += "'";
            }
        }*/

        // Get daily ridership data from past 365 available days
        const xhttpDaily = new XMLHttpRequest();
        xhttpDaily.onload = function() {
            const response = JSON.parse(this.responseText);
            
            // Weekly
            let weeklyRidership = 0;
            let maxDailyRidershipWeekly = 0;
            let maxDailyDateWeekly;
            for (let i=0; i<7; i++) {
                let dailyRidership = 0;
                if (element == 'subway') dailyRidership = parseInt(response[i].subways_total_estimated_ridership);
                else if (element == 'bus') dailyRidership = parseInt(response[i].buses_total_estimated_ridersip);

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
                if (element == 'subway') dailyRidership = parseInt(response[i].subways_total_estimated_ridership);
                else if (element == 'bus') dailyRidership = parseInt(response[i].buses_total_estimated_ridersip);
                
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

            if (element == 'subway') {
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
            else if (element == 'bus') {
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

            test += weeklyRidership;
            document.getElementById('totalweeklytransitrides').innerHTML = test.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        //xhttpDaily.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$where=" + dateString);
        xhttpDaily.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$limit=365&$order=date+DESC");
        xhttpDaily.send();

        // Get hourly ridership data from past 365 available days
        const xhttpHourly = new XMLHttpRequest();
    }

    loadData('subway');
    loadData('bus');
}