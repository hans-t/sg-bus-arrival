(function(){
    var input = document.getElementById('bus-stop-id-input');
    input.onchange = function(event) {
        if (this.checkValidity()) {
            loadArrivalData(this.value);
        }
    }
})()


function loadArrivalData(busStopId) {
    var request = new XMLHttpRequest();
    request.addEventListener('load', renderData);
    request.open('GET', '/' + busStopId, true);
    request.responseType = 'json';
    request.send();
}


function renderData(event){
    var busArrivalData = event.target.response;
    var currentTime = new Date(busArrivalData.currentTime);
    console.log(busArrivalData);

    var resultTable = document.getElementById('arrival-table');
    cleanUpTable(resultTable);
    var busServices = busArrivalData.Services;
    for (var i=0; i<busServices.length; i++) {
        var busService = busServices[i];
        var serviceNo = busService.ServiceNo;
        var nextBusArrival = getTimeDiff(currentTime, new Date(busService.NextBus.EstimatedArrival));
        var subsequentBusArrival = getTimeDiff(currentTime, new Date(busService.SubsequentBus.EstimatedArrival));
        var subsequentBus3Arrival = getTimeDiff(currentTime, new Date(busService.SubsequentBus3.EstimatedArrival));
        var busStatus = busService.Status;
        var rowData = [serviceNo, nextBusArrival, subsequentBusArrival, subsequentBus3Arrival, busStatus];
        var row = createRow(rowData);
        resultTable.appendChild(row);
    }
}

function cleanUpTable(table) {
    while (table.children.length > 1) {
        table.removeChild(table.lastChild);
    }
}


function getTimeDiff(currentTime, arrivalTime) {
    var delta = (arrivalTime - currentTime) / 1000;
    var minutes = Math.floor(delta/60);
    delta -= minutes * 60;
    var seconds = Math.floor(delta % 60);
    return minutes.toString() + ':' + ('0' + seconds.toString()).slice(-2);
}


function createRow(rowData) {
    var tr = document.createElement('tr');
    for (var i=0; i<rowData.length; i++) {
        var td = document.createElement('td');
        var data = rowData[i];
        var tdValue = document.createTextNode(data);
        td.appendChild(tdValue);
        tr.appendChild(td);
    }
    return tr
}