"""A demo of OpenFRET library usage for CSV files."""

import csv
import os
import json
from datetime import date
from typing import List
from openfret import Channel, Trace, Dataset, Metadata, read_data, write_data


def load_csv_traces(root_folder: str) -> Dataset:
    """Loads FRET traces from CSV files within a root folder.

    Args:
        root_folder: The path to the root folder containing the CSV files.
                     Subfolders within this folder are assumed to be labels.

    Returns:
        A Dataset object containing the loaded traces.
    """

    traces: List[Trace] = []
    dataset_title = os.path.basename(root_folder)  # Use folder name as title

    for label in os.listdir(root_folder):
        label_folder = os.path.join(root_folder, label)
        if os.path.isdir(label_folder):  # only process subfolders
            for filename in os.listdir(label_folder):
                if filename.endswith(".csv"):
                    filepath = os.path.join(label_folder, filename)
                    try:
                        with open(filepath, 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            header = next(reader) # Assume first row is header

                            # Identify channels based on header.  Assume all columns are data channels.
                            channels = []
                            for i, channel_name in enumerate(header):
                                data = []
                                for row in reader:
                                    try: # Handle potential errors in data conversion
                                        data.append(float(row[i]))
                                    except ValueError:
                                        print(f"Warning: Skipping invalid data in {filepath}, row: {row}")
                                if data: # only create the channel if there is data
                                    channels.append(Channel(channel_type=channel_name, data=data))


                            if channels: # only create trace if channels were created
                                trace_metadata = Metadata({"label": label, "filename": filename})
                                traces.append(Trace(channels=channels, metadata=trace_metadata))
                            else:
                                print(f"Warning: No valid data channels found in {filepath}")
                    except Exception as e:
                        print(f"Error loading {filepath}: {e}")

    return Dataset(title=dataset_title, traces=traces)


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

