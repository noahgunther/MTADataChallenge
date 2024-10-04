// Todo:
// Data:
// - Use Pythonanywhere to host and daily update data cache
// -- Example request: https://data.ny.gov/resource/wujg-7c2s.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&station_complex_id=160&$where=transit_timestamp+between+%272024-09-17T00:00:00%27+and+%272024-09-24T23:00:00%27&$order=transit_timestamp+DESC&$limit=5000
// - Figure out what live data is possible to access and include (Today).
// - Get most popular stations / stops from hourly dataset - if possible, set up for weekly popularity!
// - Get Roosevelt island tram data from hourly dataset - if possible, set up for weekly popularity!
// - If weekly data from hourly set is possible, modify dates to use most recent weekly
// Data vis:
// - Create dynamic graphs / charts.
// - Create JS for google map embedding for stations / stops.
// CSS:
// - Create CSS for live data (old style LCD cells)
// - Create CSS for map borders
// - Make text bigger generally when other stuff is done
// JS functionality:
// - Add dropdowns arrows for more info / individual sources to panels (e.g. number of individual riders estimated at two trips per rider. source: mta.whatever, links to view raw data)
// - Write script for subway cars / buses layout and scroll or animation
// - Write autoscroll button functionality
// - Create JS for "back to top" scroll animation
// Graphics:
// - Create graphics for: Subway header (subway logo), Bus header (bus logo), DMV logo (?), subway cars, buses, motor cars, parking spots, bus line logos
// - Place subway / bus graphics according to popular stations / stops etc
// - Create custom google map style to look like MTA map?
// $$$:
// - Look into new hosting for full noahgunther.com site, including this subsite (hostgator?)
// - Pay for pythonanywhere plan to handle more traffic?

import './style.css'

window.addEventListener("load", init, false);

function init() {

    // Get data from web app
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        const response = JSON.parse(this.responseText);
        const dateMostRecent = response.dateMostRecent;
        const dateWeekStart = response.dateWeekStart;
        const dateYearStart = response.dateYearStart;

        document.getElementById('weekdaterange').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('weekdaterangetram').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('weekdaterangesubway').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('weekdaterangebus').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('yeardaterange').innerHTML = dateYearStart + ' - ' + dateMostRecent;

        document.getElementById('tramweeklyridership').innerHTML = response.tramWeeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

        document.getElementById('subwayweeklyridership').innerHTML = response.subwayWeeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailyridership').innerHTML = response.subwayMaxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailycars').innerHTML = (response.subwayMaxDailyRidershipWeekly / 200).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailydate0').innerHTML = response.subwayMaxDailyDateWeekly;
        document.getElementById('subwaymaxdailydate1').innerHTML = response.subwayMaxDailyDateWeekly;

        document.getElementById('subwaymaxannualday').innerHTML = response.subwayMaxAnnualDay;
        document.getElementById('subwaymaxannualdaymean').innerHTML = response.subwayMaxAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwayminannualday').innerHTML = response.subwayMinAnnualDay;
        document.getElementById('subwayminannualdaymean').innerHTML = response.subwayMinAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwayyearlyridership').innerHTML = response.subwayYearlyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaydailyridershipavg').innerHTML = (response.subwayYearlyRidership / 365.0).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    
        document.getElementById('busweeklyridership').innerHTML = response.busWeeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('busmaxdailyridership').innerHTML = response.busMaxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('busmaxdailybuses').innerHTML = (response.busMaxDailyRidershipWeekly / 200).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('busmaxdailydate0').innerHTML = response.busMaxDailyDateWeekly;
        document.getElementById('busmaxdailydate1').innerHTML = response.busMaxDailyDateWeekly;
        
        document.getElementById('busmaxannualday').innerHTML = response.busMaxAnnualDay;
        document.getElementById('busmaxannualdaymean').innerHTML = response.busMaxAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('busminannualday').innerHTML = response.busMinAnnualDay;
        document.getElementById('busminannualdaymean').innerHTML = response.busMinAnnualDayMeanRidership.toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('busyearlyridership').innerHTML = response.busYearlyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('busdailyridershipavg').innerHTML = (response.busYearlyRidership / 365.0).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    xhttp.open("GET", "https://gunthern.pythonanywhere.com/");
    xhttp.send();

    /*const tileColors = ['123', '456', '7', 'ACE', 'BDFM', 'G', 'JZ', 'L', 'NQRW', 'S'];
    const tileDivs = document.getElementsByClassName('tilediv');
    const tileCol = tileColors[Math.floor(Math.random() * tileColors.length)];
    for (let i=0; i<tileDivs.length; i++) {
        tileDivs[i].style = 'background-image: url(./media/tile' + tileCol + '.png);'
    }*/

    let offset = window.scrollY;

    // Parallax scroll for clouds
    const clouds = document.getElementsByClassName('cloud');
    let cloudPosY = [];
    for (let i=0; i<clouds.length; i++) {
        cloudPosY.push(parseFloat(clouds[i].style.marginTop.slice(0, -1)));
    }
    const cloudScrollYSpeed = 0.5;

    function cloudPositioner() {
        for (let i=0; i<clouds.length; i++) {
            const pos = cloudPosY[i] - 500 + offset * cloudScrollYSpeed;
            clouds[i].style.marginTop = pos + 'px';
        }
    }
    cloudPositioner();

    // Scroll animation for tram
    const tram = document.getElementById('tram');
    const tramRig = document.getElementById('tramrig');
    const tramPosY = parseFloat(tramRig.style.marginTop.slice(0, -1));
    const tramScrollLock = 1800;
    const tramScrollUnlock = 4200;
    const tramScrollXSpeed = 0.8;
    const tramScrollYSpeed = 0.8;
    function tramPositioner() {
        const pos = -1200 + offset * tramScrollXSpeed;
        tram.style.marginLeft = pos + 'px';
        if (offset > tramScrollLock) {
            if (offset < tramScrollUnlock) {
                tramRig.style.marginTop = (tramPosY + (offset - tramScrollLock) * tramScrollYSpeed) + 'px';
            }
            else {
                tramRig.style.marginTop = (tramPosY + (tramScrollUnlock - tramScrollLock) * tramScrollYSpeed) + 'px';
            }
        }
    }
    tramPositioner();

    window.addEventListener("scroll", function() {
        offset = window.scrollY;
        cloudPositioner();
        tramPositioner();
    });
}