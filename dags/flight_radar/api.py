import requests
from mongodb.functions import get_non_ended_flight_records,get_non_started_flight_records
import math
from datetime import datetime, timezone, timedelta

def get_flight_summary_from_flight_first_seen(auth,flight_datetime_from,flight_datetime_to,airports,categories):


    url = "https://fr24api.flightradar24.com/api/flight-summary/full"
    params = {
        'airports': airports,
        'categories': categories,
        'flight_datetime_from': flight_datetime_from,
        'flight_datetime_to': flight_datetime_to
    }

    headers = {
    'Accept': 'application/json',
    'Accept-Version': 'v1',
    'Authorization': f'Bearer {auth}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


flight_ids = '3b380c80,3b380c9c,3b380cc4'


def get_flight_summary_from_flight_id(auth,flight_ids,airports,categories):
    
    url = "https://fr24api.flightradar24.com/api/flight-summary/full"
    params = {
        'airports': airports,
        'categories': categories,
        'flight_ids': flight_ids
    }

    headers = {
    'Accept': 'application/json',
    'Accept-Version': 'v1',
    'Authorization': f'Bearer {auth}'
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def get_non_ended_flight_ids(threshold_time,max_flight_ids_input):
    # print(threshold_time)
    non_ended_flight_list = get_non_ended_flight_records(threshold_time)

    if len(non_ended_flight_list) >0:

        non_ended_flight_list_ids = []

        for data in non_ended_flight_list:
            non_ended_flight_list_ids.append(data['_id'])

        flight_id_list_to_be_sent_for_status_check = []
        string_input = ''
        start = 0
        for _ in range(0,int(math.ceil(len(non_ended_flight_list_ids)/max_flight_ids_input))):

            for flight_id in non_ended_flight_list_ids[start: start + max_flight_ids_input]:
                string_input += flight_id
                string_input += ','

            flight_id_list_to_be_sent_for_status_check.append(string_input[:-1])
            start += max_flight_ids_input
            string_input = ''

        return flight_id_list_to_be_sent_for_status_check

    else:
        print(f"No data exists for live flights before {threshold_time}")
        return []


def get_non_started_flight_ids(threshold_time,max_flight_ids_input):
    # print(threshold_time)
    non_started_flight_list = get_non_started_flight_records(threshold_time)

    if len(non_started_flight_list) >0:

        non_started_flight_list_ids = []

        for data in non_started_flight_list:
            non_started_flight_list_ids.append(data['_id'])

        flight_id_list_to_be_sent_for_status_check = []
        string_input = ''
        start = 0
        for _ in range(0,int(math.ceil(len(non_started_flight_list_ids)/max_flight_ids_input))):

            for flight_id in non_started_flight_list_ids[start: start + max_flight_ids_input]:
                string_input += flight_id
                string_input += ','

            flight_id_list_to_be_sent_for_status_check.append(string_input[:-1])
            start += max_flight_ids_input
            string_input = ''

        return flight_id_list_to_be_sent_for_status_check

    else:
        print(f"No data exists for live flights before {threshold_time}")
        return []