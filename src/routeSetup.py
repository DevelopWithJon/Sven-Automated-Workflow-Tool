from enum import Enum
from geopy import distance as geodis
import json
import pandas as pd
import requests
from Random_Order_Generator import randomGenerator
import time
from utils.constants import US_STATE_ABB_MAP


GEOLOCATE = "http://api.positionstack.com/v1/forward?access_key="
API = "AIzaSyB6Lwiy8_Mgt71agC0ClD1RIeFiDvhqrMg"
API2 = "d562d77d1f1a2dbc9b087e827faf63fe"


def get_data(payload=None):
    if payload is None:
        test_num = int(input())

        test_data = randomGenerator(test_num)
        payload = test_data
    for record in payload:
        location = location_formatter(record["State"], record["City"])
        record["location"] = location
        geo_request = requests.get(GEOLOCATE+ API2 + "&query=" + location)
        if geo_request.status_code == 200:
            geo_json = json.loads(geo_request.text)
            record["coordinates"] = (geo_json["data"][0]["latitude"],geo_json["data"][0]["longitude"])
        else:
            time.sleep(1)
            print("needed to sleep")
            geo_json = json.loads(geo_request.text)
            record["coordinates"] = (geo_json["data"][0]["latitude"],geo_json["data"][0]["longitude"])
    return payload

def location_formatter(state,city):

    location = city + "," + US_STATE_ABB_MAP[state]
    return location

def display_matrix(matrix, location_map):
    
    print(pd.DataFrame(matrix, columns=location_map.values(), index=location_map.values()))
     


def ad_matrix(payload=None):
    if not payload:
        payload = get_data()
    if len(payload)<2:
        return "payload too small"

    # setup location list


    locations_list = [record["location"] for record in payload]
    matrix = [[[] for _ in range(len(locations_list))] for _ in range(len(locations_list))]

    
    location_map = {i: locations_list[i] for i in range(len(locations_list))}

    for i in range(len(locations_list)):
        for j in range(len(locations_list)):
            if i == j:
                matrix[i][j] = 0
            else:
                matrix[i][j] = geodis.distance(payload[i]["coordinates"],payload[j]["coordinates"]).miles
        
    return matrix, location_map
