// Todo:
// Data:
// - Figure out what live data is possible to access and include (Today)
// - Get hourly popularity of week for subway
// - Get most popular bus stops for the week from hourly dataset (most pop station, most pop in each borough, whole list)
// - Get hourly popularity of week for bus
// - Review all code / math
// - Add dropdowns arrows for more info / individual sources to panels (e.g. source: mta.whatever, links to view raw data)
// -- Add data disclaimers (estimated from ...) and info on updating (most recent data from mta sets fetch daily at https://gunthern.pythonanywhere.com/, most recent update xxxxxx)
// Data vis:
// - Create dynamic graphs / charts.
// CSS:
// - Create CSS for live data (old style LCD cells)
// - Do a pass for various screen widths, general functionality
// JS functionality:
// - Write script for subway cars, buses, subway platform (from inside train) scroll or animation (like the tramway)
// - Test on mobile
// Graphics:
// - Create graphics for: Subway header (subway icon), Bus header (bus icon), subway cars, buses, bus line logos(?)
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
        document.getElementById('weekdaterangesubway0').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('weekdaterangesubway1').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('weekdaterangesubway2').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('weekdaterangebus').innerHTML = dateWeekStart + ' - ' + dateMostRecent;
        document.getElementById('yeardaterange0').innerHTML = dateYearStart + ' - ' + dateMostRecent;
        document.getElementById('yeardaterange1').innerHTML = dateYearStart + ' - ' + dateMostRecent;

        document.getElementById('tramweeklyridership').innerHTML = response.tramWeeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('trammaxdailyridership').innerHTML = response.tramMaxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('trammaxdailydate').innerHTML = response.tramMaxDailyDateWeekly;

        document.getElementById('subwayweeklyridership').innerHTML = response.subwayWeeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailyridership0').innerHTML = response.subwayMaxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailyridership1').innerHTML = response.subwayMaxDailyRidershipWeekly.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailycars').innerHTML = (response.subwayMaxDailyRidershipWeekly / 200).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        document.getElementById('subwaymaxdailydate0').innerHTML = response.subwayMaxDailyDateWeekly;
        document.getElementById('subwaymaxdailydate1').innerHTML = response.subwayMaxDailyDateWeekly;

        let maxBoroughId = 'subwayweekly';
        let maxBorough = response.subwayStationMaxRidershipWeeklyBorough[0];
        if (maxBorough == 'Bronx') {
            maxBoroughId += 'bronx';
            maxBorough = 'The Bronx';
        }
        else if (maxBorough == 'Brooklyn') maxBoroughId += 'brooklyn';
        else if (maxBorough == 'Manhattan') maxBoroughId += 'manhattan';
        else if (maxBorough == 'Queens') maxBoroughId += 'queens';
        else if (maxBorough == 'Staten Island') maxBoroughId += 'staten';
        document.getElementById(maxBoroughId).hidden = true;
        document.getElementById(maxBoroughId + 'icons').hidden = true;

        let nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[0].toString());
        lineIconsFromIds(nameIds[0], 'subwaystationweekmaxstationserviceicons', 0);
        document.getElementById('subwaystationweekmaxstation0').innerHTML = nameIds[1];
        document.getElementById('subwaystationweekmaxstation1').innerHTML = nameIds[1];
        document.getElementById('subwaystationweekmaxborough').innerHTML = maxBorough;
        document.getElementById('subwaystationweekmaxcount').innerHTML = response.subwayStationMaxRidershipWeeklyCount[0].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

        if (maxBorough != 'The Bronx') {
            let bronxMaxStationIndex;
            for (let i=0; i<response.subwayStationMaxRidershipWeeklyBorough.length; i++) {
                if (response.subwayStationMaxRidershipWeeklyBorough[i] == 'Bronx') {
                    bronxMaxStationIndex = i;
                    break;
                }
            }
            nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[bronxMaxStationIndex].toString());
            lineIconsFromIds(nameIds[0], 'subwayweeklybronxicons', 0);
            document.getElementById('subwaybronxweekmaxstation0').innerHTML = nameIds[1];
            document.getElementById('subwaybronxweekmaxstation1').innerHTML = nameIds[1];
            document.getElementById('subwaybronxweekmaxcount').innerHTML = response.subwayStationMaxRidershipWeeklyCount[bronxMaxStationIndex].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        if (maxBorough != 'Brooklyn') {
            let brooklynMaxStationIndex;
            for (let i=0; i<response.subwayStationMaxRidershipWeeklyBorough.length; i++) {
                if (response.subwayStationMaxRidershipWeeklyBorough[i] == 'Brooklyn') {
                    brooklynMaxStationIndex = i;
                    break;
                }
            }
            nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[brooklynMaxStationIndex].toString());
            lineIconsFromIds(nameIds[0], 'subwayweeklybrooklynicons', 0);
            document.getElementById('subwaybrooklynweekmaxstation0').innerHTML = nameIds[1];
            document.getElementById('subwaybrooklynweekmaxstation1').innerHTML = nameIds[1];
            document.getElementById('subwaybrooklynweekmaxcount').innerHTML = response.subwayStationMaxRidershipWeeklyCount[brooklynMaxStationIndex].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        if (maxBorough != 'Manhattan') {
            let manhattanMaxStationIndex;
            for (let i=0; i<response.subwayStationMaxRidershipWeeklyBorough.length; i++) {
                if (response.subwayStationMaxRidershipWeeklyBorough[i] == 'Manhattan') {
                    manhattanMaxStationIndex = i;
                    break;
                }
            }
            nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[manhattanMaxStationIndex].toString());
            lineIconsFromIds(nameIds[0], 'subwayweeklymanhattanicons', 0);
            document.getElementById('subwaymanhattanweekmaxstation0').innerHTML = nameIds[1];
            document.getElementById('subwaymanhattanweekmaxstation1').innerHTML = nameIds[1];
            document.getElementById('subwaymanhattanweekmaxcount').innerHTML = response.subwayStationMaxRidershipWeeklyCount[manhattanMaxStationIndex].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        if (maxBorough != 'Queens') {
            let queensMaxStationIndex;
            for (let i=0; i<response.subwayStationMaxRidershipWeeklyBorough.length; i++) {
                if (response.subwayStationMaxRidershipWeeklyBorough[i] == 'Queens') {
                    queensMaxStationIndex = i;
                    break;
                }
            }
            nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[queensMaxStationIndex].toString());
            lineIconsFromIds(nameIds[0], 'subwayweeklyqueensicons', 0);
            document.getElementById('subwayqueensweekmaxstation0').innerHTML = nameIds[1];
            document.getElementById('subwayqueensweekmaxstation1').innerHTML = nameIds[1];
            document.getElementById('subwayqueensweekmaxcount').innerHTML = response.subwayStationMaxRidershipWeeklyCount[queensMaxStationIndex].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        if (maxBorough != 'Staten Island') {
            let statenMaxStationIndex;
            for (let i=0; i<response.subwayStationMaxRidershipWeeklyBorough.length; i++) {
                if (response.subwayStationMaxRidershipWeeklyBorough[i] == 'Staten Island') {
                    statenMaxStationIndex = i;
                    break;
                }
            }
            nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[statenMaxStationIndex].toString());
            lineIconsFromIds(nameIds[0], 'subwayweeklystatenicons', 0);
            document.getElementById('subwaystatenweekmaxstation0').innerHTML = nameIds[1];
            document.getElementById('subwaystatenweekmaxstation1').innerHTML = nameIds[1];
            document.getElementById('subwaystatenweekmaxcount').innerHTML = response.subwayStationMaxRidershipWeeklyCount[statenMaxStationIndex].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
        let subwayWeeklyTableHtmlString = "<tr><th><text>Rank</text></th><th><text>Subway Station / Service</text></th><th><text>Borough</text></th><th><text>Ridership (week)</text></th></tr>";
        for (let i=0; i<response.subwayStationMaxRidershipWeeklyStation.length; i++) {
            const nameIds = idsNameSplit(response.subwayStationMaxRidershipWeeklyStation[i].toString());
            let idsImgString = '<br/>';
            for (let j=0; j<nameIds[0].length; j++) {
                idsImgString += '<img src="./media/subway' + nameIds[0][j] + '.png"></img>';
            }
            let tableString = "<tr><th><text>" + (i+1) + "</text></th><th><text>" + nameIds[1] + "</text>" + idsImgString + "</th>";
            tableString += "<th><text>" + response.subwayStationMaxRidershipWeeklyBorough[i] + "</text></th>";
            tableString += "<th><text>" + response.subwayStationMaxRidershipWeeklyCount[i].toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + "</text></th></tr>";
            subwayWeeklyTableHtmlString += tableString;
        }
        document.getElementById('subwayweeklytable').innerHTML = subwayWeeklyTableHtmlString;

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
        
        document.getElementById('subwayweeklystationcomparison').setAttribute('src', 'https://gunthern.pythonanywhere.com/weeklystationcomparison?dummy' + Date.now())
        console.log('https://gunthern.pythonanywhere.com/weeklystationcomparison?dummy' + Date.now());

        updateScrollValues();
    }
    xhttp.open("GET", "https://gunthern.pythonanywhere.com/");
    xhttp.send();

    // Extract subway line identifiers from station name
    function idsNameSplit(nameIds) {

        const regex = /\(([^)]+)\)/g;
        let match;
        const result = [];
        let name = nameIds;
        while ((match = regex.exec(nameIds)) !== null) {
            const r = match[1].split(',');
            let matchFound = false;
            for (let i=0; i<r.length; i++) {
                if (r[i].length == 1 || r[i] == 'SIR') {
                    result.push(r[i]);
                    matchFound = true;
                }
            }
            if (matchFound) {
                name = name.replace(match.toString().match(/\([^)]*\)/g), '').trim();
            }
        }
        return [result, name]

    }

    // Create HTML for subway line icons from line ids
    function lineIconsFromIds(id, element, scale) {

        // Create html string
        let htmlString = '';
        let logoScale = ['sublogo'];
        for (let i=0; i<id.length; i++) {
            htmlString += '<img class="' + logoScale[scale] + '" ';
            if (i==0) htmlString += 'style="margin-left: 10px;" ';
            htmlString += 'src = "./media/subway' + id[i].toString() + '.png"></img>';
        }
        
        // Update html
        document.getElementById(element).innerHTML = htmlString;
    }

    // Dropdown behavior

    // Subway table
    const subwayStationTableToggle0 = document.getElementById('togglesubwaystationtabledropdown0');
    const subwayStationTableToggle0Text = document.getElementById('subwaystationtabledropdowntext');
    const subwayStationTableToggle0Arrow = document.getElementById('subwaystationtabledropdownarrow');
    const subwayStationTableToggle1 = document.getElementById('togglesubwaystationtabledropdown1');
    const subwayStationTable = document.getElementById('subwaystationtabledropdown');
    subwayStationTableToggle0.addEventListener('click', function() {
        toggleSubwayStationTable(false);
    });
    subwayStationTableToggle1.addEventListener('click', function() { 
        toggleSubwayStationTable(true);
    });
    function toggleSubwayStationTable(scrollIntoView) {
        if (subwayStationTable.hidden) {
            subwayStationTable.hidden = false;
            subwayStationTableToggle0Text.innerHTML = "Hide all stations by ridership: ";
            subwayStationTableToggle0Arrow.style.transform = "rotate(0deg)";
        }
        else {
            subwayStationTable.hidden = true;
            subwayStationTableToggle0Text.innerHTML = "View all stations by ridership: ";
            subwayStationTableToggle0Arrow.style.transform = "rotate(180deg)";
            if (scrollIntoView) subwayStationTableToggle0.scrollIntoView();
        }
        updateScrollValues();
    }

    // Scrolling effects
    let offset;
    let tramStart;
    let docEnd;
    function updateScrollValues() {
        offset = window.scrollY;
        tramStart = document.getElementById('tramanimstart').getBoundingClientRect().bottom + window.scrollY;
        docEnd = document.getElementById('end').getBoundingClientRect().bottom + window.scrollY;
    }
    updateScrollValues();

    // Parallax scroll for clouds
    const clouds = document.getElementsByClassName('cloud');
    let cloudPosY = [];
    for (let i=0; i<clouds.length; i++) {
        cloudPosY.push(parseFloat(clouds[i].style.marginTop.slice(0, -1)));
    }
    const cloudScrollYSpeed = 0.5;

    function cloudPositioner() {
        for (let i=0; i<clouds.length; i++) {
            const pos = cloudPosY[i] - tramStart + 4500 + offset * cloudScrollYSpeed;
            clouds[i].style.marginTop = pos + 'px';
        }
    }
    cloudPositioner();

    // Scroll animation for tram
    const tram = document.getElementById('tram');
    const tramRig = document.getElementById('tramrig');
    const tramPosY = parseFloat(tramRig.style.marginTop.slice(0, -1));
    const tramScrollLock = tramStart - 3100;
    const tramScrollUnlock = tramScrollLock + 2200;
    const tramScrollXSpeed = 0.66;
    const tramScrollYSpeed = 0.9;
    function tramPositioner() {
        const pos = offset * tramScrollXSpeed;
        const offsetX = tramStart / 100;
        tram.style.marginLeft = (pos/20 - offsetX) + '%';
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

    // Autoscroll
    function scrollTo(destination, duration) {
        if (duration <= 0) {
            return;
        }
        const difference = destination.scrollTop - window.scrollY;
        const perTick = (difference / duration) * 10;
    
        setTimeout(() => {
            window.scrollTo(0, window.scrollY + perTick);
            if (window.scrollY === destination.scrollTop) {
                return;
            }
            scrollTo(destination, duration - 10);
        }, 10);
    }
    const footermiddle = document.getElementById('footermiddle');
    const footerleft = document.getElementById('footerleft');
    footermiddle.addEventListener('click', function() { scrollTo(document.getElementById('top'), 1000); });
    footerleft.addEventListener('click', function() { scrollTo(document.getElementById('top'), 1000); });

    updateScrollValues();
}