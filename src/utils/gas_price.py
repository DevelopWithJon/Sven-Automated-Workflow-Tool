import json
import requests
import time

import logging

from configs import EPA_API

logging.basicConfig(filename="example.log", encoding="utf-8")
LOGGER = logging.getLogger(__name__)


def get_gas_price(API_KEY):
    url = f"https://api.eia.gov/series/?api_key={EPA_API}&series_id=TOTAL.DFONUUS.M"
    gas_price_request = requests.get(url)
    if gas_price_request.status_code == 200:
        gas_price_json = json.loads(gas_price_request.text)

    else:
        time.sleep(1)
        LOGGER.info("API needed an additional second")
        gas_price_json = json.loads(gas_price_request.text)
    return gas_price_json["series"][0]["data"][0][1]
