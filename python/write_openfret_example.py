# -*- coding: utf-8 -*-
"""
Example of creating and writing an OpenFRET data (JSON) file

"""

from openfret import Dataset, Trace, Channel, Metadata, write_data
from datetime import date
import numpy as np

filename = "fret_data.json" # Output file name

# Simulate a 100-frame-long trace as random noise (donor only, no dynamics).
ch1data = np.random.normal(loc=1000.0,scale=200.0,size=100).tolist() # Donor, mean intensity = 1000
ch2data = np.random.normal(loc=0.0,scale=200.0,size=100).tolist() # Acceptor, mean intensity = 0

# Create Channel objects to store intensity versus time series for each illumination/detection condition within a trace
#   Keywords optional if order is maintained
#   Units for wavelengths:   nm (nanometers)
#   Units for exposure_time: seconds
#   data MUST refer to a 1-dimensional list of intensity values (either of type float or int)
channel1 = Channel(channel_type="donor", 
                   data=ch1data, 
                   excitation_wavelength=532.0, 
                   emission_wavelength=585.0, 
                   exposure_time=0.1)
channel2 = Channel(channel_type="acceptor", 
                   data=ch2data, 
                   excitation_wavelength=640.0, 
                   emission_wavelength=680.0, 
                   exposure_time=0.1)

# Create a Trace object comprising one or more channels
#   Keywords optional if order is maintained
#   channels argument must be a 1D list of Channel objects or a single Channel object
trace1 = Trace(channels=[channel1, channel2], metadata=Metadata({"molecule_id": "1"}))

# Create a Dataset object
dataset = Dataset(
    title="My FRET Experiment",
    traces=[trace1], # 1D list of all traces in dataset (just one trace in this example)
    description="FRET data of protein folding",
    experiment_type="2-Color FRET",
    authors=["John Doe", "Jane Smith"],
    institution="University X",
    date=date(2024, 1, 1),
    metadata=Metadata({"experiment_id": "20240101_JD_JS_1", "movie_file": "20240101_CoolExperiment.TIF"}),
    sample_details={"buffer_conditions": "Phosphate buffer", "other_details": Metadata({"pH": 7.4})}, #Example of nested metadata
    instrument_details={"microscope": "Olympus IX83", "other_details": Metadata({"objective": "60x oil 1.5 NA"})}, #Example of nested metadata
)

# Create (empty) traces and add them to previously created Dataset (note: using dataset.traces.append() will NOT work)
trace2 = Trace(channels=[Channel(channel_type="donor",data=[]),Channel(channel_type="acceptor",data=[])])
trace3 = Trace(channels=[Channel(channel_type="donor",data=[]),Channel(channel_type="acceptor",data=[])])
dataset.add([trace2, trace3])

# Add channel data to empty traces
trace2.channels[0].data = np.random.normal(loc=1000.0,scale=200.0,size=100).tolist()
trace2.channels[0].data = np.random.normal(loc=0,scale=200.0,size=100).tolist()
trace3.channels[1].data = np.random.normal(loc=1000.0,scale=200.0,size=100).tolist()
trace3.channels[1].data = np.random.normal(loc=0,scale=200.0,size=100).tolist()

# Set excitation and emission wavelengths for all traces in dataset
dataset.set(channel_type="donor", excitation_wavelength=532.0, emission_wavelength=585.0)
dataset.set(channel_type="acceptor", excitation_wavelength=640.0, emission_wavelength=680.0)
dataset.set(exposure_time=0.1) # Omit channel_type to set parameter for all channels in dataset

# Write the dataset to a JSON file
write_data(dataset, "fret_data.json")