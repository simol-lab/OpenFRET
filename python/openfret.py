"""Python library for handling the openFRET data format."""

# to do:
    # Warn user if channels within a trace contain different numbers of frames
    # Raise error if traces argument for Dataset is not a 1D list of Trace objects

import json
from warnings import warn
from datetime import date
from typing import List, Dict, Any, Optional

class Metadata(dict):
    """User-defined metadata."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Channel:
    """Represents a single data channel."""
    def __init__(self, channel_type: str, data: List[float] = None, excitation_wavelength: Optional[float] = None,
                 emission_wavelength: Optional[float] = None, exposure_time: Optional[float] = None, metadata: Optional[Metadata] = None):
        self.channel_type = channel_type
        self._data = None
        if data is not None:
            self.data = data
        self.excitation_wavelength = excitation_wavelength
        self.emission_wavelength = emission_wavelength
        self.exposure_time = exposure_time
        self.metadata = metadata or Metadata()
        
    @property
    def data(self):
        return self._data
    
    @data.setter # Validate type and value of data argument
    def data(self,value):
        if not isinstance(value,list):
            raise TypeError("data must be a list. Please check data argument and ensure it is a 1-D list of type float")
        if not all(not isinstance(item,list) for item in value):
            raise ValueError("data must be a single, 1-dimensional (non-nested) list")
        if not (all(isinstance(item,float) for item in value) or all(isinstance(item,int) for item in value)):
            raise ValueError("Contents of data list must numbers of identical type (float or int).")
        self._data = value

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
        self._channels = None
        if channels is not None:
            self.channels = channels
        self.metadata = metadata or Metadata()
        
    @property
    def channels(self):
        return self._channels
    
    @channels.setter # Validate channel argument
    def channels(self,value):
        if not isinstance(value,Channel) and (not isinstance(value,list)):
            raise TypeError("channels property must either be a Channel object or a single, 1-dimensional (non-nested) list")
        if isinstance(value,list):
            if not all(isinstance(item,Channel) for item in value):
                raise ValueError("Contents of channels list must be Channel objects.")
        if isinstance(value,list):
            channel_lengths = []
            for item in value:
                channel_lengths.append(len(item.data))
            if len(set(channel_lengths))>1:
                warn("Channels provided to Trace object are not all of equal length! Please check that this is intended.")
            self._channels = value
        else:
            self._channels = [value] # If a single Channel is provided outside of a list, convert to 1-element list

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

