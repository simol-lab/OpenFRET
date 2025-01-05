import unittest
import json
from datetime import date
from openfret import Dataset, Trace, Channel, Metadata, write_data, read_data
import os

class TestOpenFret(unittest.TestCase):

  def test_channel_creation(self):
    """Tests creating a Channel object with all and some parameters."""
    channel_all = Channel(
        channel_type="donor",
        data=[1, 2, 3],
        excitation_wavelength=488,
        emission_wavelength=525,
        exposure_time=0.1,
        metadata=Metadata({"key": "value"})
    )

    channel_some = Channel("acceptor", [4, 5, 6])

    self.assertEqual(channel_all.channel_type, "donor")
    self.assertEqual(channel_all.data, [1, 2, 3])
    self.assertEqual(channel_all.excitation_wavelength, 488)
    self.assertEqual(channel_all.emission_wavelength, 525)
    self.assertEqual(channel_all.exposure_time, 0.1)
    self.assertEqual(channel_all.metadata["key"], "value")

    self.assertEqual(channel_some.channel_type, "acceptor")
    self.assertEqual(channel_some.data, [4, 5, 6])
    self.assertIsInstance(channel_some.metadata, Metadata)  # Check if empty metadata is created

  def test_channel_to_dict_from_dict(self):
    """Tests converting Channel objects to and from dictionaries."""
    channel = Channel("donor", [10, 20, 30], 450, 530, 0.2, {"gain": 2})
    channel_dict = channel.to_dict()

    self.assertEqual(channel_dict["channel_type"], "donor")
    self.assertEqual(channel_dict["data"], [10, 20, 30])
    self.assertEqual(channel_dict["excitation_wavelength"], 450)
    self.assertEqual(channel_dict["emission_wavelength"], 530)
    self.assertEqual(channel_dict["exposure_time"], 0.2)
    self.assertEqual(channel_dict["metadata"]["gain"], 2)

    reconstructed_channel = Channel.from_dict(channel_dict)

    self.assertEqual(reconstructed_channel.channel_type, channel.channel_type)
    self.assertEqual(reconstructed_channel.data, channel.data)
    self.assertEqual(reconstructed_channel.excitation_wavelength, channel.excitation_wavelength)
    self.assertEqual(reconstructed_channel.emission_wavelength, channel.emission_wavelength)
    self.assertEqual(reconstructed_channel.exposure_time, channel.exposure_time)
    self.assertEqual(reconstructed_channel.metadata["gain"], channel.metadata["gain"])

  def test_trace_creation(self):
    """Tests creating a Trace object with and without metadata."""
    channels = [Channel("donor", [1, 2, 3]), Channel("acceptor", [4, 5, 6])]
    trace_metadata = Metadata({"temperature": 25})
    trace_no_metadata = Trace(channels)
    trace_with_metadata = Trace(channels, trace_metadata)

    self.assertEqual(trace_no_metadata.channels, channels)
    self.assertIsInstance(trace_no_metadata.metadata, Metadata)  # Check if empty metadata is created
    self.assertEqual(trace_with_metadata.channels, channels)
    self.assertEqual(trace_with_metadata.metadata, trace_metadata)

  def test_trace_to_dict_from_dict(self):
    """Tests converting Trace objects to and from dictionaries."""
    channels = [Channel("donor", [7, 8, 9]), Channel("acceptor", [10, 11, 12])]
    trace = Trace(channels, Metadata({"condition": "control"}))
    trace_dict = trace.to_dict()

    self.assertEqual(len(trace_dict["channels"]), len(channels))
    self.assertEqual(trace_dict["metadata"]["condition"], "control")

    reconstructed_trace = Trace.from_dict(trace_dict)

    self.assertEqual(len(reconstructed_trace.channels), len(channels))

  def test_dataset_creation(self):
    """Tests creating a Dataset object with all and some parameters."""
    channels1 = [Channel("donor", [1, 2]), Channel("acceptor", [3, 4])]
    channels2 = [Channel("donor", [5, 6]), Channel("acceptor", [7, 8])]
    traces = [Trace(channels1), Trace(channels2)]
    metadata = Metadata({"experiment": "FRET"})
    sample_details = {"buffer": "PBS"}
    instrument_details = {"laser": "640nm"}
    test_date = date(2024, 1, 1)

    dataset_all = Dataset(
        title="Test Dataset",
        traces=traces,
        description="A test dataset",
        experiment_type="smFRET",
        authors=["John Doe", "Jane Doe"],
        institution="Test University",
        date=test_date,
        metadata=metadata,
        sample_details=sample_details,
        instrument_details=instrument_details,
    )

    dataset_some = Dataset(title="Another Dataset", traces=traces)

    self.assertEqual(dataset_all.title, "Test Dataset")
    self.assertEqual(len(dataset_all.traces), 2)
    self.assertEqual(dataset_all.description, "A test dataset")
    self.assertEqual(dataset_all.experiment_type, "smFRET")
    self.assertEqual(dataset_all.authors, ["John Doe", "Jane Doe"])
    self.assertEqual(dataset_all.institution, "Test University")
    self.assertEqual(dataset_all.date, test_date)
    self.assertEqual(dataset_all.metadata, metadata)
    self.assertEqual(dataset_all.sample_details, sample_details)
    self.assertEqual(dataset_all.instrument_details, instrument_details)

    self.assertEqual(dataset_some.title, "Another Dataset")
    self.assertEqual(len(dataset_some.traces), 2)
    self.assertIsInstance(dataset_some.metadata, Metadata)
    self.assertEqual(dataset_some.sample_details, {})
    self.assertEqual(dataset_some.instrument_details, {})

  def test_dataset_to_dict_from_dict(self):
    """Tests converting Dataset objects to and from dictionaries."""
    channels1 = [Channel("donor", [1, 2]), Channel("acceptor", [3, 4])]
    channels2 = [Channel("donor", [5, 6]), Channel("acceptor", [7, 8])]
    traces = [Trace(channels1), Trace(channels2)]
    test_date = date(2024, 2, 29) # Test leap year
    dataset = Dataset(
        title="Test Dataset",
        traces=traces,
        description="A test dataset",
        date=test_date,
        metadata={"global": "info"},
        sample_details={"ph": 7.4},
        instrument_details={"camera": "EMCCD"}
    )

    dataset_dict = dataset.to_dict()
    reconstructed_dataset = Dataset.from_dict(dataset_dict)

    self.assertEqual(reconstructed_dataset.title, dataset.title)
    self.assertEqual(len(reconstructed_dataset.traces), len(dataset.traces))
    self.assertEqual(reconstructed_dataset.description, dataset.description)
    self.assertEqual(reconstructed_dataset.date, dataset.date)
    self.assertEqual(reconstructed_dataset.metadata, dataset.metadata)
    self.assertEqual(reconstructed_dataset.sample_details, dataset.sample_details)
    self.assertEqual(reconstructed_dataset.instrument_details, dataset.instrument_details)


  def test_write_read_data(self):
    """Tests writing and reading Dataset objects to/from JSON files."""
    channels1 = [Channel("donor", [9, 8]), Channel("acceptor", [7, 6])]
    traces = [Trace(channels1)]
    test_date = date(2024, 3, 15)
    dataset = Dataset(title="File I/O Test", traces=traces, date=test_date, description="This is a test", metadata={"test":"metadata"})
    filename = "test_data.json"

    write_data(dataset, filename)
    loaded_dataset = read_data(filename)

    self.assertEqual(loaded_dataset.title, dataset.title)
    self.assertEqual(len(loaded_dataset.traces), len(dataset.traces))
    self.assertEqual(loaded_dataset.date, dataset.date)
    self.assertEqual(loaded_dataset.description, dataset.description)
    self.assertEqual(loaded_dataset.metadata, dataset.metadata)

    os.remove(filename) # Clean up the test file

if __name__ == "__main__":
    unittest.main()