import time
from datetime import datetime, timezone, timedelta
from mongodb.functions import update_collection, create_collection
from flight_radar.api import get_non_ended_flight_ids, get_flight_summary_from_flight_first_seen, get_flight_summary_from_flight_id,get_non_started_flight_ids
from api_helper.functions import get_time_range_as_per_sync_frequency

auth = '<write auth token here>'

airports= 'BLR'
categories= 'P'


def check_collection():
    ## Create collection if not exists
    create_collection()


def add_new_flights(data_interval_end):

    start_datetime_str,end_datetime_str = get_time_range_as_per_sync_frequency(5,30,base_time=data_interval_end)

    ## SCRIPT TO ADD NEW FLIGHTS
    flight_datetime_from= start_datetime_str
    flight_datetime_to= end_datetime_str
    data = get_flight_summary_from_flight_first_seen(auth,flight_datetime_from,flight_datetime_to,airports,categories)

    # data = {'data':
    #         [{'fr24_id': 'test_1', 'flight': 'EY237', 'callsign': 'ETD237', 'operating_as': 'ETD', 'painted_as': 'ETD', 'type': 'A21N', 'reg': 'A6-AES', 'orig_icao': 'VOBL', 'orig_iata': 'BLR', 'datetime_takeoff': '2025-07-12T10:54:34Z', 'runway_takeoff': '27R', 'dest_icao': 'OMAA', 'dest_iata': 'AUH', 'dest_icao_actual': 'OMAA', 'dest_iata_actual': 'AUH', 'datetime_landed': '2025-07-12T14:07:38Z', 'runway_landed': '31R', 'flight_time': 11584, 'actual_distance': 2736.7, 'circle_distance': 2726.33, 'category': 'Passenger', 'hex': '896678', 'first_seen': '2025-07-12T10:42:16Z', 'last_seen': '2025-07-12T14:08:47Z', 'flight_ended': False}
    #          ,{'fr24_id': 'test_2', 'flight': '6E478', 'callsign': 'IGO478', 'operating_as': 'IGO', 'painted_as': 'IGO', 'type': 'A21N', 'reg': 'VT-ILH', 'orig_icao': 'VIAR', 'orig_iata': 'ATQ', 'datetime_takeoff': '2025-07-12T10:42:18Z', 'runway_takeoff': '34', 'dest_icao': 'VOBL', 'dest_iata': 'BLR', 'dest_icao_actual': 'VOBL', 'dest_iata_actual': 'BLR', 'datetime_landed': '2025-07-12T13:27:25Z', 'runway_landed': '27L', 'flight_time': 9907, 'actual_distance': 2157.24, 'circle_distance': 2070.41, 'category': 'Passenger', 'hex': '80141F', 'first_seen': '2025-07-12T10:42:31Z', 'last_seen': '2025-07-12T13:41:42Z', 'flight_ended': False}
    #          ,{'fr24_id': 'test_3', 'flight': '6E7363', 'callsign': 'IGO7363', 'operating_as': 'IGO', 'painted_as': 'IGO', 'type': 'AT76', 'reg': 'VT-IRQ', 'orig_icao': 'VOBL', 'orig_iata': 'BLR', 'datetime_takeoff': '2025-07-12T10:47:51Z', 'runway_takeoff': '27R', 'dest_icao': 'VOML', 'dest_iata': 'IXE', 'dest_icao_actual': 'VOML', 'dest_iata_actual': 'IXE', 'datetime_landed': '2025-07-12T11:37:52Z', 'runway_landed': '24', 'flight_time': 3001, 'actual_distance': 320.481, 'circle_distance': 307.961, 'category': 'Passenger', 'hex': '801754', 'first_seen': '2025-07-12T10:42:36Z', 'last_seen': '2025-07-12T11:38:48Z', 'flight_ended': False}
    #          ]}

    data_list = data['data']


    if len(data_list) == 0:
        print("No Data Found")

    else:
        for data in data_list:
            update_collection(data)
            time.sleep(1)



def check_non_landed_flights(data_interval_end):
    ### SCRIPT TO UPDATE LIVE FLIGHTS ( Landed / Not Landed ) - we check every 3 hrs

    base_time = data_interval_end
    # Subtract 3 hours - check before 3 hours if there are any flights that did not land yet
    threshold_time = base_time - timedelta(hours=3)

    flight_id_list = get_non_ended_flight_ids(threshold_time, max_flight_ids_input=10)

    if len(flight_id_list) > 0:

        for flight_ids in flight_id_list:
            data = get_flight_summary_from_flight_id(auth,flight_ids,airports,categories)

            data_list = data['data']
            if len(data_list) == 0:
                print("No Data Found")

            else:
                for data in data_list:
                    update_collection(data)
                    time.sleep(1)

    else:
        print("No Flights fall in the date threshold!!")


def check_non_takeoff_flights(data_interval_end):
    ### SCRIPT TO UPDATE FLIGHTS ( Non - Take Off Flights ) - we check every 30 minutes

    # Step 1: Get UTC time minus 30 minutes
    base_time = data_interval_end - timedelta(minutes=30)

    threshold_time = base_time

    flight_id_list = get_non_started_flight_ids(threshold_time, max_flight_ids_input=10)

    if len(flight_id_list) > 0:

        for flight_ids in flight_id_list:
            data = get_flight_summary_from_flight_id(auth,flight_ids,airports,categories)

            data_list = data['data']
            if len(data_list) == 0:
                print("No Data Found")

            else:
                for data in data_list:
                    update_collection(data)
                    time.sleep(1)

    else:
        print("No Flights fall in the date threshold!!")
