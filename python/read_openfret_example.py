# -*- coding: utf-8 -*-
"""
Example of reading an OpenFRET data (JSON) file

Run write_openfret_example.py before this, and make sure the file names match.

@author: Leyou Zhang, Alex Johnson-Buck
"""

from openfret import read_data

filename = "fret_data.json" # Input file name

# Read the dataset from a JSON file
loaded_dataset = read_data(filename)

# Access data
print(loaded_dataset.title)
for trace in loaded_dataset.traces:
    for channel in trace.channels:
        print(f"Channel type: {channel.channel_type}, Data: {channel.data}")
print(loaded_dataset.sample_details["other_details"]) #Accessing the nested metadata
print(loaded_dataset.instrument_details["other_details"]) #Accessing the nested metadata

# Or print the whole dictionary
import json
print(json.dumps(loaded_dataset.to_dict(), indent=4, default=str)) # Add default=str to handle the date object in json output