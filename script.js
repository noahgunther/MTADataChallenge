window.addEventListener("load", init, false);

function init() {

    function dateConstructor(subDays) {
        const date = new Date();
        date.setDate(date.getDate() - subDays);
        let day = date.getDate().toString();
        day.length < 2 ? day = '0' + day : day;
        let month = (date.getMonth() + 1).toString();
        month.length < 2 ? month = '0' + month : month;
        let year = date.getFullYear();
        return year + "-" + month + "-" + day;
    }

    function loadData(element, date) {
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function() {
            const response = JSON.parse(this.responseText)[0];
            if (element = 'subway') document.getElementById(element).innerHTML = response.subways_total_estimated_ridership;
            if (element = 'bus') document.getElementById(element).innerHTML = response.buses_total_estimated_ridersip;
        }
        xhttp.open("GET", "http://data.ny.gov/resource/vxuj-8kew.json?$limit=1&$$app_token=fIErfxuaUHt3vyktfOyK1XFRS&date=" + date);
        xhttp.send();
      }

    loadData('subway', dateConstructor(2));
    loadData('bus', dateConstructor(2));
}