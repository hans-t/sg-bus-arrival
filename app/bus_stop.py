from datetime import datetime

import redis
import requests

import credentials
import settings


HEADERS = {
    'AccountKey': credentials.API_KEY,
    'UniqueUserID': credentials.UNIQUE_USER_ID,
    'accept': 'application/json',
}


redis_conn = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


def get_arrival_time(bus_stop_id):
    """Get bus arrival times from API"""
    endpoint = 'http://datamall2.mytransport.sg/ltaodataservice/BusArrival'
    params = {'BusStopID': bus_stop_id}
    resp = requests.get(endpoint, params=params, headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        data['currentTime'] = datetime.utcnow().isoformat()
        return data


def get_attributes(bus_stop_id):
    """Get stored bus stop description from Redis server.
    Returns empty dictionary if bus stop ID is not found.
    """

    return redis_conn.hgetall(bus_stop_id)


def get_info(bus_stop_id):
    """Get bus stop information.
    Only check for bus arrival times if bus stop ID is valid.
    """

    attributes = get_attributes(bus_stop_id)
    if attributes:
        arrival_time = get_arrival_time(bus_stop_id)
        arrival_time.update(attributes)
        return arrival_time
    else:
        return {'Services': []}


def list_all():
    """List all bus stops with their attributes."""
    endpoint = 'http://datamall.mytransport.sg/ltaodataservice.svc/BusStopCodeSet'
    params = {'$skip': 0}
    while True:
        resp = requests.get(endpoint, params=params, headers=HEADERS)
        if resp.status_code == 200:
            yield resp.json()
            params['$skip'] += 50
        else:
            break


def iter_responses(responses):
    """Iterate over list_all() responses."""
    for response in responses:
        bus_stops = response.get('d', [])
        if bus_stops:
            yield from bus_stops
        else:
            break


def get_map():
    """Create bus stops map."""
    bus_stops = iter_responses(list_all())
    keys = ('Road', 'Description')
    return {bus_stop['Code']: {key: bus_stop[key] for key in keys} for bus_stop in bus_stops}


def dump_map_to_json(bus_stops_map):
    """Dump bus stops map as json"""
    import json
    with open(settings.BUS_STOPS_MAP_JSON_FILE, 'w', encoding='utf-8') as jsonfp:
        json.dump(bus_stops_map, jsonfp, ensure_ascii=False, sort_keys=True)


def import_map_to_redis():
    """Import bus stops map JSON file to redis"""
    import json
    with open(settings.BUS_STOPS_MAP_JSON_FILE, encoding='utf-8') as jsonfp:
        bus_stops_map = json.load(jsonfp)

    redis_conn.flushdb()
    for bus_stop_code, attributes in bus_stops_map.items():
        redis_conn.hmset(name=bus_stop_code, mapping=attributes)
    redis_conn.save()