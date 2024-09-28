window.addEventListener("load", init, false);

function init() {

    function dateConstructor(subStart, range) {
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
    }

    function loadData(element, dates) {
        let dateString = '';
        for (let i=0; i<dates.length; i++) {
            dateString += "date='" + dates[i];
            if (i != dates.length-1) {
                dateString += "' OR ";
            }
            else {
                dateString += "'";
            }
        }
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            const response = JSON.parse(this.responseText);
            let totalRidership = 0;
            for (let i=0; i<response.length; i++) {
                if (element == 'subway') totalRidership += parseInt(response[i].subways_total_estimated_ridership);
                else if (element == 'bus') totalRidership += parseInt(response[i].buses_total_estimated_ridersip);
            }
            if (element == 'subway') document.getElementById(element).innerHTML = totalRidership;
            else if (element == 'bus') document.getElementById(element).innerHTML = totalRidership;
        }
        xhttp.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&$where=" + dateString);
        xhttp.send();
    }

    loadData('subway', dateConstructor(5, 7));
    loadData('bus', dateConstructor(5, 7));
}