"""A demo of OpenFRET library usage for CSV files."""

import csv
import os
import json
from datetime import date
from typing import List
from openfret import Channel, Trace, Dataset, Metadata, read_data, write_data, load_csv_traces

"""

The load_csv_traces function definition:

def load_csv_traces(root_folder: str) -> Dataset:
    Loads FRET traces from CSV files within a root folder.

    Args:
        root_folder: The path to the root folder containing the CSV files.
                     Subfolders within this folder are assumed to be labels.

    Returns:
        A Dataset object containing the loaded traces.

"""

if __name__ == "__main__":
    # Example usage:
    root_folder = "fret_data_csv"  # Replace with your root folder path
    dataset = load_csv_traces(root_folder)
    write_data(dataset, "fret_data_from_csv.json", compress=True)

    loaded_dataset = read_data("fret_data_from_csv.json.zip")
    print(json.dumps(loaded_dataset.to_dict(), indent=4))

# Example folder structure:
# fret_data_csv/
# ├── condition_A/
# │   ├── trace1.csv
# │   └── trace2.csv
# └── condition_B/
#     ├── trace3.csv
#     └── trace4.csv

