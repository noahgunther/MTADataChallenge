// Todo:
// - Get the rest of the data needed from MTA datasets.
// - Add data for most popular stops in each borough?
// - Add some graphs for activity by borough or that kind of thing
// - Figure out what live data is possible to access and include.
// - Create CSS for tile divs (use color of popular subway line)
// - Create CSS for live data (old style LCD cells)
// - Add drop downs for more info / sources (e.g. number of individual riders estimated at two trips per rider. source: mta.whatever)
// - Create graphics for: Page top (yellow hazard edge), MTA/NG logo for header, subway header, bus header, subway cars, buses, motor cars, parking spots, subway line logos, bus line logos, general MTA seasoning
// - Write script for subway cars / buses / cars / parking spots layout and scroll or animation
// - Create JS for "back to top"
// - Other stuff: have a roosevelt island tram go by (include stats?), include map graphics or google maps link for station highlighting

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
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            const response = JSON.parse(this.responseText);
            let totalRidership = 0;
            for (let i=0; i<response.length; i++) {
                if (element == 'subway') totalRidership += parseInt(response[i].subways_total_estimated_ridership);
                else if (element == 'bus') totalRidership += parseInt(response[i].buses_total_estimated_ridersip);
            }
            if (element == 'subway') {
                document.getElementById('subwayweeklyridership').innerHTML = totalRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('subwayweeklyfaretotal').innerHTML = (totalRidership * 2.9).toFixed(3).slice(0, -1).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
            else if (element == 'bus') {
                document.getElementById('busweeklyridership').innerHTML = totalRidership.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                document.getElementById('busweeklyfaretotal').innerHTML = (totalRidership * 2.9).toFixed(3).slice(0, -1).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
        }
        //xhttp.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$where=" + dateString);
        xhttp.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$limit=7&$order=date+DESC");
        xhttp.send();
    }

    loadData('subway');
    loadData('bus');
}