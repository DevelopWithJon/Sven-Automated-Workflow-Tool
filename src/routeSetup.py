from enum import Enum
from geopy import distance as geodis
import json
import pandas as pd
import requests
from Random_Order_Generator import randomGenerator
import time
from utils.constants import US_STATE_ABB_MAP
import logging

logging.basicConfig(filename='example.log', encoding='utf-8')
LOGGER = logging.getLogger(__name__)

GEOLOCATE = "http://api.positionstack.com/v1/forward?access_key="
API = "AIzaSyB6Lwiy8_Mgt71agC0ClD1RIeFiDvhqrMg"
API2 = "d562d77d1f1a2dbc9b087e827faf63fe"
GAS_PRICE = 3.612

test_payload_v2 = [{'State': 'Alabama', 'City': 'Madison', 'Customer_Name': 'Test', 'Company': 'Test Co', 'Product': {'Generic Name': 'rosuvastatin calcium', 'Brand Name': 'Crestor', 'Price': 31.69}, 'Units': 197, 'Creation_date': '11-12-2021 20:29:135169', 'location': 'Madison,AL', 'coordinates': (34.694505, -86.757772)}, {'State': 'New Mexico', 'City': 'Albuquerque', 'Customer_Name': 'Test', 'Company': 'Test Co', 'Product': {'Generic Name': 'ibuprofen tablet', 'Brand Name': 'Motrin', 'Price': 65.81}, 'Units': 104, 'Creation_date': '11-12-2021 20:29:135169', 'location': 'Albuquerque,NM', 'coordinates': (35.128683, -106.579128)}, {'State': 'Washington', 'City': 'Yakima', 'Customer_Name': 'Test', 'Company': 'Test Co', 'Product': {'Generic Name': 'amitriptyline tablet', 'Brand Name': 'Elavil', 'Price': 43.42}, 'Units': 12, 'Creation_date': '11-12-2021 20:29:135169', 'location': 'Yakima,WA', 'coordinates': (46.593247, -120.547823)}, {'State': 'Wisconsin', 'City': 'Appleton', 'Customer_Name': 'Test', 'Company': 'Test Co', 'Product': {'Generic Name': 'amoxapine tablet', 'Brand Name': 'Amoxapine tablet', 'Price': 51.22}, 'Units': 337, 'Creation_date': '11-12-2021 20:29:135169', 'location': 'Appleton,WI', 'coordinates': (44.265929, -88.394699)}]

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
            LOGGER.info('API needed an additional second')
            geo_json = json.loads(geo_request.text)
            record["coordinates"] = (geo_json["data"][0]["latitude"],geo_json["data"][0]["longitude"])
    return payload

def location_formatter(state,city):

    location = city + "," + US_STATE_ABB_MAP[state]
    return location

def display_matrix(matrix, location_map):
    print(pd.DataFrame(matrix, columns=location_map.values(), index=location_map.values()))
    

def ad_matrix(payload=None, distribution_center=None):
    if not payload:
        payload = get_data()
    if len(payload)<2:
        LOGGER.error("payload too small")
        raise ValueError

    # setup location list
    if distribution_center:
        payload.insert(0,distribution_center)

    locations_list = [record["location"] for record in payload]
    matrix = [[[] for _ in range(len(locations_list))] for _ in range(len(locations_list))]

    
    location_map = {i: locations_list[i] for i in range(len(locations_list))}

    for i in range(len(locations_list)):
        for j in range(len(locations_list)):
            if i == j:
                matrix[i][j] = 0
            else:
                distance = geodis.distance(payload[i]["coordinates"],payload[j]["coordinates"]).miles
                cost_of_travel = distance*GAS_PRICE
                matrix[i][j] = geodis.distance(payload[i]["coordinates"],payload[j]["coordinates"]).miles
                if "Product" in payload[i]:
                    revenue_of_travel = payload[i]['Product']['Price'] * payload[i]['Units']
                    matrix[i][j] = revenue_of_travel - cost_of_travel
                else:
                    matrix[i][j] = cost_of_travel
        
    return matrix, location_map
