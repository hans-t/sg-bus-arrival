import requests
from datetime import datetime
import credentials


ROOT_URL = 'http://datamall2.mytransport.sg'
DATASET_PATH = '/ltaodataservice/BusArrival'
HEADERS = {
    'AccountKey': credentials.API_KEY,
    'UniqueUserID': credentials.UNIQUE_USER_ID,
    'accept': 'application/json',
}


def get_bus_arrivals_data(bus_stop_id):
    params = {'BusStopID': bus_stop_id}
    resp = requests.get(ROOT_URL + DATASET_PATH, params=params, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        data['currentTime'] = datetime.utcnow().isoformat()
        return data
