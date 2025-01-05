"""Python library for handling the openFRET data format."""

import json
from datetime import date
from typing import List, Dict, Any, Optional

class Metadata(dict):
    """User-defined metadata."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Channel:
    """Represents a single data channel."""
    def __init__(self, channel_type: str, data: List[float], excitation_wavelength: Optional[float] = None,
                 emission_wavelength: Optional[float] = None, exposure_time: Optional[float] = None, metadata: Optional[Metadata] = None):
        self.channel_type = channel_type
        self.data = data
        self.excitation_wavelength = excitation_wavelength
        self.emission_wavelength = emission_wavelength
        self.exposure_time = exposure_time
        self.metadata = metadata or Metadata()

    def to_dict(self):
        return {
            "channel_type": self.channel_type,
            "excitation_wavelength": self.excitation_wavelength,
            "emission_wavelength": self.emission_wavelength,
            "exposure_time": self.exposure_time,
            "data": self.data,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            channel_type=data["channel_type"],
            data=data["data"],
            excitation_wavelength=data.get("excitation_wavelength"),
            emission_wavelength=data.get("emission_wavelength"),
            exposure_time=data.get("exposure_time"),
            metadata=Metadata(data.get("metadata", {}))
        )

class Trace:
    """Represents a single-molecule trace."""
    def __init__(self, channels: List[Channel], metadata: Optional[Metadata] = None):
        self.channels = channels
        self.metadata = metadata or Metadata()

    def to_dict(self):
        return {
            "channels": [channel.to_dict() for channel in self.channels],
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            channels=[Channel.from_dict(channel_data) for channel_data in data["channels"]],
            metadata=Metadata(data.get("metadata", {}))
        )

class Dataset:
    """Represents a collection of single-molecule traces."""
    def __init__(self, title: str, traces: List[Trace], description: Optional[str] = None, experiment_type: Optional[str] = None,
                 authors: Optional[List[str]] = None, institution: Optional[str] = None, date: Optional[date] = None, metadata: Optional[Metadata] = None,
                 sample_details: Optional[Dict[str, Any]] = None, instrument_details: Optional[Dict[str, Any]] = None):

        self.title = title
        self.traces = traces
        self.description = description
        self.experiment_type = experiment_type
        self.authors = authors
        self.institution = institution
        self.date = date
        self.metadata = metadata or Metadata()
        self.sample_details = sample_details or {}
        self.instrument_details = instrument_details or {}

    def to_dict(self):
        data = {
            "title": self.title,
            "traces": [trace.to_dict() for trace in self.traces],
            "metadata": self.metadata,
            "sample_details": self.sample_details,
            "instrument_details": self.instrument_details
        }
        if self.description: data["description"] = self.description
        if self.experiment_type: data["experiment_type"] = self.experiment_type
        if self.authors: data["authors"] = self.authors
        if self.institution: data["institution"] = self.institution
        if self.date: data["date"] = self.date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            title=data["title"],
            traces=[Trace.from_dict(trace_data) for trace_data in data["traces"]],
            description=data.get("description"),
            experiment_type=data.get("experiment_type"),
            authors=data.get("authors"),
            institution=data.get("institution"),
            date=date.fromisoformat(data["date"]) if data.get("date") else None,
            metadata=Metadata(data.get("metadata", {})),
            sample_details=data.get("sample_details", {}),
            instrument_details=data.get("instrument_details", {})
        )

def write_data(dataset: Dataset, filename: str):
    """Writes the dataset to a JSON file."""
    with open(filename, "w") as f:
        json.dump(dataset.to_dict(), f, indent=4)

def read_data(filename: str) -> Dataset:
    """Reads the dataset from a JSON file."""
    with open(filename, "r") as f:
        data = json.load(f)
        return Dataset.from_dict(data)


if __name__ == "__main__":
    # Example usage:
    dataset = Dataset(
        title="My FRET Experiment",
        traces=[
            Trace(channels=[
                Channel(channel_type="donor", data=[100, 110, 120]),
                Channel(channel_type="acceptor", data=[20, 30, 40], exposure_time=0.1, metadata={"gain":1.2})
            ], metadata={"trace_condition":"high salt"}),
            Trace(channels=[
                Channel(channel_type="donor", data=[120, 110, 100]),
                Channel(channel_type="acceptor", data=[40, 30, 20])
            ])
        ],
        description="FRET experiment on DNA origami",
        date=date(2024, 1, 1),
        sample_details={"buffer_conditions":"1xPBS"},
        instrument_details={"microscope":"Olympus IX71"}
    )
    
    write_data(dataset, "fret_data.json")
    loaded_dataset = read_data("fret_data.json")
    print(json.dumps(loaded_dataset.to_dict(), indent=4))
