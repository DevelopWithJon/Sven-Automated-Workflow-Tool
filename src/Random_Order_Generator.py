"""Random Order Generator"""
import random
import datetime
from typing import Any, Dict, List

from utils.constants import DRUGS_PAYLOAD, US_CITIES_MAP


def randomGenerator(num_of_items: int) -> List[Dict[str, Any]]:
    order_dict = {}
    order_list = []
    for num in range(num_of_items):
        order_dict["State"] = random.choice(list(US_CITIES_MAP))
        order_dict["City"] = random.choice(US_CITIES_MAP[order_dict["State"]])
        order_dict["Customer_Name"] = "Test"
        order_dict["Company"] = "Test Co"
        order_dict["Product"] = random.choice(DRUGS_PAYLOAD)
        order_dict["Creation_date"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%S:%f")
        order_list.append(order_dict)
    return order_list
