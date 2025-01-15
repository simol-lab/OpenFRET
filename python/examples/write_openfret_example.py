# -*- coding: utf-8 -*-
"""
Example of creating and writing an OpenFRET data (JSON) file

Created on Wed Jan 15 12:54:14 2025

@author: Leyou Zhang, Alex Johnson-Buck
"""

from openfret import Dataset, Trace, Channel, Metadata, write_data
from datetime import date
import numpy as np

filename = "fret_data.json" # Output file name

# Simulate a 100-frame-long trace as random noise (donor only, no dynamics).
ch1data = np.random.normal(loc=1000.0,scale=200.0,size=100).tolist() # Donor, mean intensity = 1000
ch2data = np.random.normal(loc=0.0,scale=200.0,size=100).tolist() # Acceptor, mean intensity = 0

# Create Channel objects (keywords optional if order is maintained)
#   Units for wavelengths:   nm (nanometers)
#   Units for exposure_time: seconds
#   data should refer to a 1-dimensional list of intensity values
channel1 = Channel(channel_type="donor", data=ch1data, excitation_wavelength=488.0, emission_wavelength=520.0, exposure_time=0.1)
channel2 = Channel(channel_type="acceptor", data=ch2data, excitation_wavelength=532.0, emission_wavelength=580.0, exposure_time=0.1)

# Create a Trace object
trace1 = Trace([channel1, channel2], metadata=Metadata({"molecule_id": "1"}))

# Create a Dataset object
dataset = Dataset(
    title="My FRET Experiment",
    traces=[trace1], # 1D list of all traces in dataset (just one trace in this example)
    description="FRET data of protein folding",
    experiment_type="2-Color FRET",
    authors=["John Doe", "Jane Smith"],
    institution="University X",
    date=date(2024, 1, 1),
    metadata=Metadata({"experiment_id": "123"}),
    sample_details={"buffer_conditions": "Phosphate buffer", "other_details": Metadata({"ph": 7.4})}, #Example of nested metadata
    instrument_details={"microscope": "Olympus IX83", "other_details": Metadata({"objective": "60x oil 1.5 NA"})}, #Example of nested metadata
)

# Write the dataset to a JSON file
write_data(dataset, "fret_data.json")