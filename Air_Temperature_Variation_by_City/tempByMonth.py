#!/bin/python3

import requests
import calendar
from datetime import datetime
from cityIDs import getCityId


def getHighsLowsOfMonthById(month_number, year_4digit, location_id):

    # Date range parameters
    daysInMonth = calendar.monthrange(year_4digit, month_number)[1]

    start_date = datetime(year_4digit, month_number, 1).strftime("%Y-%m-%d")
    end_date = datetime(year_4digit, month_number, daysInMonth).strftime("%Y-%m-%d")


    # NOAA CDO API endpoint
    api_endpoint = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data'

    # Add toke here
    token = None #get a web services token from the NOAA

    if token == None:
        print("A web services token from the NOAA is needed.")
        print("Add the token to 'cityIDs.py' and 'tempByMonth.py'.")
        exit()

    # Data type parameters
    high_temp_data_type = 'TMAX'  # Maximum temperature
    low_temp_data_type = 'TMIN'  # Minimum temperature

    # Request headers
    headers = {
        'token': api_token
    }

    # Request query parameters for high temperatures
    params_high_temp = {
        'datasetid': 'GHCND',  # Global Historical Climatology Network - Daily (GHCND)
        'datatypeid': high_temp_data_type,
        'locationid': location_id,
        'startdate': start_date,
        'enddate': end_date,
        'limit': 1000,  # Maximum number of results per request (adjust as needed)
        'units': 'standard',  # Units of measurement
        'includemetadata': 'false'  # Exclude metadata to reduce response size
    }


    # Send GET request for high temperatures
    attempt_request = True
    
    while attempt_request:
        response_high_temp = requests.get(api_endpoint, headers=headers, params=params_high_temp)
        if response_high_temp.status_code == 200:
            attempt_request = False


    # Request query parameters for low temperatures
    params_low_temp = {
        'datasetid': 'GHCND',  # Global Historical Climatology Network - Daily (GHCND)
        'datatypeid': low_temp_data_type,
        'locationid': location_id,
        'startdate': start_date,
        'enddate': end_date,
        'limit': 1000,  # Maximum number of results per request (adjust as needed)
        'units': 'standard',  # Units of measurement
        'includemetadata': 'false'  # Exclude metadata to reduce response size
    }

    # Send GET request for low temperatures
    attempt_request = True
    
    while attempt_request:
        response_low_temp = requests.get(api_endpoint, headers=headers, params=params_low_temp)
        if response_low_temp.status_code == 200:
            attempt_request = False
    

    # Check if the requests were successful
    high_temp = []
    low_temp = []
    
    # Parse the response JSON for high temperatures
    high_temp_data = response_high_temp.json()['results']
    
    # Parse the response JSON for low temperatures
    low_temp_data = response_low_temp.json()['results']
    
    # Process the data as needed
    for high_temp_record, low_temp_record in zip(high_temp_data, low_temp_data):
        date = high_temp_record['date']
        high_temp.append(high_temp_record['value'])
        low_temp.append(low_temp_record['value'])

    return high_temp, low_temp


def getHighsLowsOfMonth(month, year, city, state):
    loc = getCityId("US", state, city)
    return getHighsLowsOfMonthById(month, year, loc)

