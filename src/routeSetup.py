"""Configure matrix."""
from geopy import distance as geodis  # type: ignore
import json
import pandas as pd
import requests
from Random_Order_Generator import randomGenerator
import time
from utils.constants import MILES_PER_GALLON, US_STATE_ABB_MAP, GAS_PRICE
from utils.configs import GEOLOCATE_API
import logging

logging.basicConfig(filename="example.log", encoding="utf-8")
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

GEOLOCATE = "http://api.positionstack.com/v1/forward?access_key="

def get_data(payload=None, gen_items=None):
    if payload is None:
        test_data = randomGenerator(int(gen_items))
        payload = test_data

    for record in payload:
        location = location_formatter(record["State"], record["City"])
        record["location"] = location
        geo_request = requests.get(GEOLOCATE + GEOLOCATE_API + "&query=" + location)
        try:
            geo_json = json.loads(geo_request.text)
            record["coordinates"] = (
                geo_json["data"][0]["latitude"],
                geo_json["data"][0]["longitude"],
            )
        except:
            time.sleep(1)
            LOGGER.info("API needed an additional second")
            geo_json = json.loads(geo_request.text)
            record["coordinates"] = (
                geo_json["data"][0]["latitude"],
                geo_json["data"][0]["longitude"],
            )
            
    return payload


def location_formatter(state, city):

    location = city + ", " + US_STATE_ABB_MAP[state]
    return location


def display_matrix(matrix, location_map):
    print(
        pd.DataFrame(matrix, columns=location_map.values(), index=location_map.values())
    )


def ad_matrix(payload, distribution_center):

    if len(payload) < 2:
        LOGGER.error("payload too small")
        raise ValueError

    # setup location list
    if distribution_center:
        payload.insert(0, distribution_center)

    locations_list = [record["location"] for record in payload]
    matrix = [
        [[] for _ in range(len(locations_list))] for _ in range(len(locations_list))
    ]

    location_map = {i: locations_list[i] for i in range(len(locations_list))}

    for i in range(len(locations_list)):
        for j in range(len(locations_list)):
            if i == j:
                matrix[i][j] = 0
            else:
                distance = geodis.distance(
                    payload[i]["coordinates"], payload[j]["coordinates"]
                ).miles
                cost_of_travel = (distance / MILES_PER_GALLON) * GAS_PRICE
                matrix[i][j] = geodis.distance(
                    payload[i]["coordinates"], payload[j]["coordinates"]
                ).miles
                if "Product" in payload[i]:
                    revenue_of_travel = payload[i]["Price"] * payload[i]["Units"]
                    matrix[i][j] = revenue_of_travel - cost_of_travel
                    # Case for distribution center
                else:
                    matrix[i][j] = cost_of_travel

    return matrix, location_map
