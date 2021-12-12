"""Random Order Generator."""
import random
import datetime
from typing import Any, Dict, List

from utils.constants import DRUGS_PAYLOAD, US_CITIES_MAP, DISTRIBUTION_CENTER_MAP

KEYS = ["State", "City", "Customer_Name", "Company"]

def randomGenerator(num_of_items: int) -> List[Dict[str, Any]]:
    """Combine dictions to list"""

    order_list = []
    for _ in range(num_of_items):
        order_list.append(dicBuilder())
    return order_list

def dicBuilder():
    """Builds dictionaries"""
    order_dict = {}
    order_dict["State"] = list(US_CITIES_MAP)[random.randint(0,49)]
    order_dict["City"] = US_CITIES_MAP[order_dict["State"]][random.randint(0,len(US_CITIES_MAP[order_dict["State"]])-1)]
    order_dict["Customer_Name"] = "Test"
    order_dict["Company"] = "Test Co"
    order_dict["Product"] = DRUGS_PAYLOAD[random.randint(0,323)]
    order_dict["Units"] = random.randint(10,500)
    order_dict["Creation_date"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%S:%f")
    return order_dict

d = randomGenerator(2)
d.append(DISTRIBUTION_CENTER_MAP[0])
print(d)