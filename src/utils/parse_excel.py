"""Collect and parse email attachments"""
import pandas as pd
import os
import datetime

from utils.constants import DRUGS_PAYLOAD
from shortestRoute import assign_to_warehouse

cdir = os.getcwd()
attachment_path = cdir + "/attachments/"

template = pd.read_excel(cdir + "/templates/Excel_Template.xlsx")

def make_df(order_record):
    if order_record.endswith(".csv"):
        df = pd.read_csv(attachment_path+order_record)
    else:
        df = pd.read_excel(attachment_path+order_record)
    return df

def compare_to_template(df):
    if list(df.columns)[0:6] == list(template.columns)[0:6]:
        return True
    return False

def parse_orders(order_payload):
    order_list = []
    for record in order_payload:
        df = make_df(record)
        if compare_to_template(df):
            for index, series in df.iterrows():
                order_list.append(dicBuilder(series))
    return assign_to_warehouse(order_list)
    

def dicBuilder(series):
    """Build order dictionaries"""
    order_dict = {}
    order_dict["State"] = series["State"]
    order_dict["City"] = series["City"]
    order_dict["Customer_Name"] = series["Name"]
    order_dict["Company"] = series["Company"]
    order_dict["Product"] = series["Product"]
    order_dict["Price"] = DRUGS_PAYLOAD[order_dict["Product"]]
    order_dict["Units"] = series["Units"]
    order_dict["Creation_date"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%S:%f")
    return order_dict
