"""Collect and parse email data"""
from Typing import Any
import pandas as pd
import os
cdir = os.getcwd()
template = pd.read_excel(cdir + "/templates/Excel_Template.xlsx")

print(template.columns)

def payload_to_pandas(request_payload):
    if request_payload.endswith(".csv"):
        return pd.read_csv(request_payload)
    elif request_payload.endswith((".xlsx", "xls")):
        return pd.read_excel
def validate_format(template: Any, request_payload: Any, client_email: str) -> None:
    """validate if request fits required format."""
    payload = payload_to_pandas(request_payload)
    
    if payload.columns != template.columns:
        send_error_email(client_email)
    
def send_error_email(client_email)
    