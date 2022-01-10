"""Collect and parse email data"""
from typing import Any
import pandas as pd
import os

dirname = os.path.dirname
abs = dirname(dirname(os.path.abspath(__file__)))
template = pd.read_excel(abs + "\Excel_Template.xlsx")


def payload_to_pandas(request_payload):
    if request_payload.endswith(".csv"):
        return pd.read_csv(request_payload)
    elif request_payload.endswith((".xlsx", "xls")):
        return pd.read_excel


def validate_format(template: Any, request_payload: Any, client_email: str) -> None:
    """validate if request fits required format."""
    payload = payload_to_pandas(request_payload)

    if payload.columns != template.columns:
        print("no match")
