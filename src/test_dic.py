"""Collect and parse email data"""
import pandas as pd
import os
cdir = os.getcwd()
tempate = pd.read_excel(cdir + "/templates/Excel_Template.xlsx")