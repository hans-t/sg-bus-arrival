import unittest
import unittest.mock as mock

import bus_stop


patcher = mock.patch('bus_stop.requests')
requests_mock = patcher.start()

patcher = mock.patch('bus_stop.redis')
redis_mock = patcher.start()


class Response:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data


class TestGetArrivalTime(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch('bus_stop.datetime')
        self.addCleanup(patcher.stop)
        self.datetime_mock = patcher.start()
        self.now = '2016-03-07T13:09:53.373022'
        self.datetime_mock.utcnow.return_value.isoformat.return_value = self.now

    def test_200_returns_json_data(self):
        json_data = {
            'BusStopID': '83139',
            'Services': [
                {"ServiceNo": "15"},
            ],
        }
        requests_mock.get.return_value = Response(data=json_data, status_code=200)
        output = bus_stop.get_arrival_time('83139')
        json_data['currentTime'] = self.now
        self.assertEqual(output, json_data)

    def test_non_200_returns_empty_services(self):
        # obsolete
        requests_mock.get.return_value = Response(data={'Services': []}, status_code=500)
        output = bus_stop.get_arrival_time('83140')
        self.assertEqual(output, None)

    def test_non_200_returns_placeholder(self):
        requests_mock.get.return_value = Response(data={'Services': []}, status_code=500)
        output = bus_stop.get_arrival_time('83140')
        self.assertEqual(output, {'placeholder': None})


class TestGetInfo(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch('bus_stop.get_attributes')
        self.addCleanup(patcher.stop)
        self.get_attributes_mock = patcher.start()

        patcher = mock.patch('bus_stop.get_arrival_time')
        self.addCleanup(patcher.stop)
        self.get_arrival_time_mock = patcher.start()

    def test_valid_bus_stop_returns_arrival_data_with_bus_stop_details(self):
        arrival_data = {
            'BusStopID': '83279',
            'Services': [
                {"ServiceNo": "15"},
            ],
        }
        self.get_arrival_time_mock.return_value = arrival_data
        self.get_attributes_mock.return_value = {'Road': 'Tuas Ave 7', 'Description': 'Opp Blk 37'}
        output = bus_stop.get_info('83219')
        arrival_data['Road'] = 'Tuas Ave 7'
        arrival_data['Description'] = 'Opp Blk 37'
        self.assertEqual(output, arrival_data)

    def test_invalid_bus_stop_returns_empty_services(self):
        # obsolete
        self.get_attributes_mock.return_value = {}
        output = bus_stop.get_info('83279')
        self.assertEqual(output, {'Services': []})

    def test_invalid_bus_stop_returns_placeholder(self):
        self.get_attributes_mock.return_value = {}
        output = bus_stop.get_info('83279')
        self.assertEqual(output, {'placeholder': None})


if __name__ == '__main__':
    unittest.main()