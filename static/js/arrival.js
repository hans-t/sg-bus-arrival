(function(){
    /* Attach event handler to input. */
    var input = document.getElementById('bus-stop-id-input');
    input.oninput = function(event) {
        if (this.checkValidity()) {
            loadBusStopInfo(this.value);
        }
    }
})()


function loadBusStopInfo(busStopId) {
    var request = new XMLHttpRequest();
    request.addEventListener('load', renderData);
    request.open('GET', '/api/bus_stop/' + busStopId, true);
    request.responseType = 'json';
    request.send();
}


function renderData(event){
    var busStopInfo = event.target.response;
    var currentTime = new Date(busStopInfo.currentTime);
    console.log(busStopInfo);

    var busStopDescSpan = document.getElementById('bus-stop-desc-p');
    busStopDescSpan.textContent = getBusStopDesc(busStopInfo);

    var resultTable = document.getElementById('bus-stop-data-tbody');
    cleanUpTable(resultTable);

    var busServices = busStopInfo.Services;
    for (var i=0; i<busServices.length; i++) {
        var busService = busServices[i];
        var row = [
            {
                'key': 'serviceNo',
                'value': busService.ServiceNo,
                'class': 'data-service-no'
            },
            {
                'key': 'nextBusArrival',
                'value': getTimeDiff(currentTime, busService.NextBus.EstimatedArrival),
                'class': 'data-next-bus-arrival'
            },
            {
                'key': 'secondBusArrival',
                'value': getTimeDiff(currentTime, busService.SubsequentBus.EstimatedArrival),
                'class': 'data-second-bus-arrival'
            },
            {
                'key': 'thirdBusArrival',
                'value': getTimeDiff(currentTime, busService.SubsequentBus3.EstimatedArrival),
                'class': 'data-third-bus-arrival'
            },
            {
                'key': 'busStatus',
                'value': busService.Status,
                'class': 'data-bus-service-status'
            }
        ]
        renderRowToTable(resultTable, row);
    }
}


function getBusStopDesc(busStopInfo) {
    if (busStopInfo.hasOwnProperty('Description')) {
        return busStopInfo['Description'] + ' (' + busStopInfo['Road'] + ')'
    } else {
        return 'Incorrect bus stop number.'
    }
}


function cleanUpTable(table) {
    while (table.firstChild) {
        table.removeChild(table.lastChild);
    }
}


function getTimeDiff(currentTime, arrivalTimeString) {
    if (arrivalTimeString) {
        var arrivalTime = new Date(arrivalTimeString);
        var delta = (arrivalTime - currentTime) / 1000;
        var minutes = Math.floor(delta/60);
        delta -= minutes * 60;
        var seconds = Math.floor(delta % 60);
        return minutes.toString() + ':' + ('0' + seconds.toString()).slice(-2);
    } else {
        return ''
    }
}


function renderRowToTable(table, row) {
    var tr = document.createElement('tr');
    for (var i=0; i<row.length; i++) {
        var td = document.createElement('td');
        var data = row[i];
        var tdValue = document.createTextNode(data.value);
        td.appendChild(tdValue);
        td.className = data.class;
        tr.appendChild(td);
    }
    table.appendChild(tr);
}