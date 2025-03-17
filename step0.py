import os
import json
import pandas as pd
from step2_create_fil_CM import process_data
from step3_CM_to_summary import process_causal_maps
from main import all_brand_summary

input_file_name = "overall_data_new_demand.csv"
col_list = ['year', 'month', 'channel', 'demand_YoY', 'ATHL_demand_contribution_YoY', 'BR_demand_contribution_YoY', 'ON_demand_contribution_YoY', 'GAP_demand_contribution_YoY']

year = 2024
month = 9
channel = 'ONL'
overall = True

all_brand_summary(year, month, channel, input_file_name , col_list, overall, "All")
