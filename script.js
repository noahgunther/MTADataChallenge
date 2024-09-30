// Todo:
// Data:
// - Figure out what live data is possible to access and include.
// - Get the rest of the data needed from MTA datasets.
// - Calculate fare data based on hourly data set and fare amounts
// - Get most popular route and line(s) servicing that route
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
// - Tile divider color(s) based on most popular subway line / station
// - Add dropdowns arrows for more info / individual sources to panels (e.g. number of individual riders estimated at two trips per rider. source: mta.whatever, links to view raw data)
// - Write script for subway cars / buses / cars / parking spots layout and scroll or animation
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

            let weeklyRidership = 0;
            let yearlyRidership = 0;

            // Weekly
            for (let i=0; i<7; i++) {
                if (element == 'subway') weeklyRidership += parseInt(response[i].subways_total_estimated_ridership);
                else if (element == 'bus') weeklyRidership += parseInt(response[i].buses_total_estimated_ridersip);
            }

            // Yearly
            for (let i=0; i<response.length; i++) {
                if (element == 'subway') yearlyRidership += parseInt(response[i].subways_total_estimated_ridership);
                else if (element == 'bus') yearlyRidership += parseInt(response[i].buses_total_estimated_ridersip);
            }

            if (element == 'subway') {
                document.getElementById('subwayweeklyridership').innerHTML = weeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                //document.getElementById('subwayweeklyfaretotal').innerHTML = (weeklyRidership * 2.9).toFixed(3).slice(0, -1).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwayyearlyridership').innerHTML = yearlyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwaydailyridershipavg').innerHTML = (yearlyRidership / 365.0).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
            else if (element == 'bus') {
                document.getElementById('busweeklyridership').innerHTML = weeklyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                //document.getElementById('busweeklyfaretotal').innerHTML = (weeklyRidership * 2.9).toFixed(3).slice(0, -1).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busyearlyridership').innerHTML = yearlyRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busdailyridershipavg').innerHTML = (yearlyRidership / 365.0).toFixed(0).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
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