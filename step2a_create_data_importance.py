"""
One time executable for creating KPI significance bins.
"""

import os
import json
import pandas as pd
import pickle

def create_discretizer(data):
    numeric_data = data.select_dtypes([float, int])
    interval_range = {}
    for col in numeric_data:
        _, labels = pd.cut(numeric_data[col].abs(), bins=3, retbins=True, labels = ['low', 'medium', 'high'])
        labels[0] = 0
        labels[-1] = float("inf")
        interval_range[col] = pd.arrays.IntervalArray.from_breaks(labels)

    return interval_range


if __name__ == "__main__":
    
    data_path = ""
    data_filename = "Brand_data_mock.csv"

    data = pd.read_csv(os.path.join(data_path, data_filename))
    # data = data.loc[:, ~data.columns.str.contains(r'\bprice\b', case=False, regex=True)]

    interval_range = create_discretizer(data)

    with open(os.path.join(data_path, "discretizer.pkl"), "wb") as f:
        pickle.dump(interval_range, f)
    