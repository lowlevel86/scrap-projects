#!/bin/python3

import requests


def getCityId(COUNTRY, STATE, CITY):

    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2/"

    # Add toke here
    token = None #get a web services token from the NOAA

    if token == None:
        print("A web services token from the NOAA is needed.")
        print("Add the token to 'cityIDs.py' and 'tempByMonth.py'.")
        exit()

    headers = {'token':token}

    attempt_request = True
    
    while attempt_request:
        r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locations?locationcategoryid=CITY&datacategoryid=TEMP&limit=1000&offset=1000', headers=headers)
        if r.status_code == 200:
            attempt_request = False
    
    json = r.json()
    cityID = ""
    for result in json['results']:
        country = result['name'].split(" ")[-1]
        state = result['name'].split(" ")[-2]
        city = result['name'].split(", ")[0]
        if (country == COUNTRY):
            if (state == STATE):
                if (city == CITY):
                    cityID = result['id']
    
    if (cityID == ""):
        print("Could not find city.")
        exit()
    else:
        return cityID

