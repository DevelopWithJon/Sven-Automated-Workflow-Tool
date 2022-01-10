"""Random Order Generator."""
import random
import datetime
from typing import Any, Dict, List

from utils.constants import DRUGS_PAYLOAD, US_CITIES_MAP

KEYS = ["State", "City", "Customer_Name", "Company"]


def randomGenerator(num_of_items: int) -> List[Dict[str, Any]]:
    """Combine to list"""

    order_list = []
    for _ in range(num_of_items):
        order_list.append(dicBuilder())
    return order_list


def dicBuilder():
    """Builds dictionaries"""
    order_dict = {}
    order_dict["State"] = list(US_CITIES_MAP)[random.randint(0, 49)]
    order_dict["City"] = US_CITIES_MAP[order_dict["State"]][
        random.randint(0, len(US_CITIES_MAP[order_dict["State"]]) - 1)
    ]
    order_dict["Customer_Name"] = "Test"
    order_dict["Company"] = "Test Co"
    order_dict["Product"] = list(DRUGS_PAYLOAD)[
        random.randint(0, len(DRUGS_PAYLOAD) - 1)
    ]
    order_dict["Price"] = DRUGS_PAYLOAD[order_dict["Product"]]
    order_dict["Units"] = random.randint(10, 60)
    order_dict["Creation_date"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%S:%f")
    return order_dict
