# -*- coding: utf-8 -*-
"""
Example of creating an OpenFRET (JSON) file from CSV files containing trace data

"""

from openfret import Dataset, Metadata, write_data
from datetime import date

# Specify filenames of CSVs containing trace 
# Note: CSVs must be rectangular; fill in any missing values in CSV with NaN before importing
donor_filename = 'donor_traces.csv'
acceptor_filename = 'acceptor_traces.csv'

# Initialize Dataset 
dataset = Dataset(
    title="My FRET Experiment",
    traces=[], # Traces is empty list to be imported from CSV files
    description="FRET data of protein folding",
    experiment_type="2-Color FRET",
    authors=["John Doe", "Jane Smith"],
    institution="University X",
    date=date(2024, 1, 1),
    metadata=Metadata({"experiment_id": "20240101_JD_JS_1", "movie_file": "20240101_CoolExperiment.TIF"}),
    sample_details={"buffer_conditions": "Phosphate buffer", "other_details": Metadata({"pH": 7.4})}, #Example of nested metadata
    instrument_details={"microscope": "Olympus IX83", "other_details": Metadata({"objective": "60x oil 1.5 NA"})}, #Example of nested metadata
)

# Import donor and acceptor traces from CSV files
dataset.from_csv(channel_type='donor',filename=donor_filename,traces_in='rows')
dataset.from_csv(channel_type='acceptor',filename=acceptor_filename,traces_in='rows')

# Set excitation and emission wavelengths for all traces in dataset
dataset.set(channel_type="donor", excitation_wavelength=532.0, emission_wavelength=585.0)
dataset.set(channel_type="acceptor", excitation_wavelength=640.0, emission_wavelength=680.0)
dataset.set(exposure_time=0.1) # Omit channel_type to set parameter for all channels in dataset

# Write the dataset to a JSON file
write_data(dataset, "fret_data.json")