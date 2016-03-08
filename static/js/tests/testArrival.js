QUnit.test("Test getting bus stop description", function(assert) {
    var busStopInfo = {
        'Description': 'Opp Blk 20A',
        'Road': 'Jalan Angklung'
    };
    assert.equal(getBusStopDesc(busStopInfo), 'Opp Blk 20A (Jalan Angklung)')
    assert.equal(getBusStopDesc({}), 'Incorrect bus stop number.')
})


QUnit.test("Test cleaning up table", function(assert) {
    var tbody = document.createElement('tbody');
    tbody.innerHTML = '<tr><td>row 1</td></tr><tr><td>row 2</td></tr>';
    cleanUpTable(tbody);
    assert.equal(tbody.innerHTML, '');
})


QUnit.test("Test get time difference", function(assert) {
    var currentTime = new Date('2016-03-08T15:54:17.558847');
    assert.equal(getTimeDiff(currentTime, '2016-03-08T15:56:18.000047'), '2:00');
    assert.equal(getTimeDiff(currentTime, '2016-03-08T15:56:17.000047'), '1:59');
    assert.equal(getTimeDiff(currentTime, ''), '');
})


QUnit.test("Test rendering row as table", function(assert) {
    function testRow(row) {
        var table = document.getElementById('bus-stop-data-tbody');
        renderRowToTable(table, row);
        var tr = table.firstChild;
        var tdElements = tr.getElementsByTagName('td');
        for (var j=0; j<tdElements.length; j++) {
            var td = tdElements[j];
            var rowElement = row[j];
            assert.equal(td.textContent, rowElement.value);
            assert.equal(td.className, rowElement.class);
        }
    }

    testRow([
        {'key': 'serviceNo','value': '199','class': 'data-service-no'},
        {'key': 'nextBusArrival','value': '1:02','class': 'data-next-bus-arrival'},
        {'key': 'secondBusArrival','value': '5:38','class': 'data-second-bus-arrival'},
        {'key': 'thirdBusArrival','value': '12:29','class': 'data-third-bus-arrival'},
        {'key': 'busStatus','value': 'In Operation','class': 'data-bus-service-status'}
    ]);
})