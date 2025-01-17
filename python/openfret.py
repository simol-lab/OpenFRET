"""Python library for handling the openFRET data format."""

import json
from datetime import date
import numpy as np
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
        self._data = None
        if data is not None:
            self.data = data
        self.excitation_wavelength = excitation_wavelength
        self.emission_wavelength = emission_wavelength
        self.exposure_time = exposure_time
        self.metadata = metadata or Metadata()
        
    @property
    def data(self):
        return self._data.copy()
    
    @data.setter 
    def data(self,value):
        ''' Validate data'''
        if not isinstance(value,list):
            raise TypeError("Channel data must be a list. Please check data argument and ensure it is a 1-D list of float or int numbers")
        if not all(not isinstance(item,list) for item in value):
            raise ValueError("Channel data must be a single, 1-dimensional (non-nested) list")
        if not (all(isinstance(item,float) for item in value) or all(isinstance(item,int) for item in value)):
            raise ValueError("Contents of Channel data list must be numbers of identical type (float or int).")
        self._data = value

    def add(self,frames: List=[]): # Controlled method to data frames to an existing channel
        if len(self._data)>0: # If current data is not empty, ensure that data type matches current contents
            datatype = type(self._data[0])
            if isinstance(frames,list): 
                if any(not isinstance(frame,datatype) for frame in frames):
                   raise ValueError(f"Elements of list passed to Channel.add() must match the datatype of the original list {datatype}")
                self._data.extend(frames)
            elif isinstance(frames,datatype):
                self._data.append(frames)
            else:
                raise TypeError(f"New elements passed to Channel.add() must match the datatype of the original list {datatype}")
        elif isinstance(frames,list):
            if not(all(isinstance(frame,int) for frame in frames) or all(isinstance(frame,float) for frame in frames)): 
                raise ValueError('Elements of list passed to Channel.add() must be of int or float type')
            self._data.extend(frames)
        elif isinstance(frames,int) or isinstance(frames,float):
            self._data.append(frames)
        else:
            raise TypeError('Channel.add() argument must be an int, float, or list of int or float numbers')

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
        return self._channels.copy()
    
    @channels.setter 
    def channels(self,value):
        ''' Validate channel '''
        if (not isinstance(value,Channel)) and (not isinstance(value,list)):
            raise TypeError("channels property must either be a Channel object created with openfret.Channel() or a single, 1-dimensional (non-nested) list of Channel objects")
        if isinstance(value,list):
            if not all(isinstance(item,Channel) for item in value):
                raise ValueError("Contents of channels list must be Channel objects created with openfret.Channel().")
        if isinstance(value,list):
            channel_lengths = []
            for item in value:
                channel_lengths.append(len(item.data))
            if len(set(channel_lengths))>1:
                print("Warning: Channels provided to Trace object are not all of equal length! Please check that this is intended.")
            self._channels = value
        else:
            self._channels = [value] # If a single Channel is provided outside of a list, convert to 1-element list
            print("Warning: Single Channel object was provided for Dataset, and converted to a one-element list")

    def add(self,channels: List[Channel]=[]): # Validate and append channels to a trace    
        if isinstance(channels,list):
            if not all(isinstance(channel,Channel) for channel in channels):
                raise ValueError('List passed to Trace.add() must contain only Channel objects')
            self._channels.extend(channels)
        elif isinstance(channels,Channel):
            self._channels.append(channels)
        else:
            raise TypeError('Only Channel objects or lists of Channel objects can be appended with Trace.add()')

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
            self._traces = None
            if traces is not None:
                self.traces = traces
            self.description = description
            self.experiment_type = experiment_type
            self.authors = authors
            self.institution = institution
            self.date = date
            self.metadata = metadata or Metadata()
            self.sample_details = sample_details or {}
            self.instrument_details = instrument_details or {}
            
    @property
    def traces(self):
        return self._traces.copy()
    
    @traces.setter 
    def traces(self,value):
        ''' Validate traces '''
        if not(isinstance(value,list)) and not(isinstance(value,Trace)): # Check if traces is either a Trace object or list
            raise TypeError('traces property of Dataset must be a list of Trace objects')
        if isinstance(value,list): 
            if any(isinstance(item,list) for item in value): 
                raise ValueError('List of traces in Dataset must be one-dimensional')
            elif not(all(isinstance(item,Trace) for item in value)):
                raise ValueError('List of traces in Dataset must contain only Trace objects created with openfret.Trace()')
            self._traces = value
        else:       
            self._traces = [value] # If traces is a single Trace object, convert to a one-element list
            print('Warning: Single Trace object was converted to a one-element list')

    def add(self,traces: List[Trace]=[]): # Controlled method to append traces to dataset
        if isinstance(traces,Trace):
            self._traces.append(traces)
        elif isinstance(traces,list): 
            if any(not isinstance(item,Trace) for item in traces):
                raise ValueError('List passed to Dataset.add() contained elements that are not Trace objects')
            self._traces.extend(traces)
        else:
            raise TypeError('Dataset.add() argument must be a Trace object or a list of Trace objects')
    
    def set(self, channel_type: Optional[str] = '', excitation_wavelength: Optional[float] = None, 
            emission_wavelength: Optional[float] = None, exposure_time: Optional[float] = None): 
        ''' Method to globally set parameters for each channel type. If channel_type is left blank or set to 'all', 
        all channels will be set accordingly. '''
        count = [0,0,0]
        for trace in self.traces:
            for channel in trace.channels:
                if channel_type == '' or channel_type == 'all' or channel.channel_type == channel_type:
                    if excitation_wavelength is not None:
                        if type(excitation_wavelength) == float:
                            channel.excitation_wavelength = excitation_wavelength
                            count[0] += 1 
                        else:
                            raise TypeError(f'excitation_wavelength must be of type float, but an argument of type {type(excitation_wavelength)} was provided.')
                    if emission_wavelength is not None:
                        if type(emission_wavelength) == float:
                            channel.emission_wavelength = emission_wavelength
                            count[1] += 1
                        else:
                            raise TypeError(f'emission_wavelength must be of type float, but an argument of type {type(emission_wavelength)} was provided.')
                    if exposure_time is not None:
                        if type(exposure_time) == float:
                            channel.exposure_time = exposure_time
                            count[2] += 1 
                        else:
                            raise TypeError(f'exposure_time must be of type float, but an argument of type {type(exposure_time)} was provided.')
        
        # Summary of what was set
        if channel_type != '':
            channel_type = channel_type + ' '
        if excitation_wavelength is not None:
            print(f'excitation_wavelength was set to {excitation_wavelength} for {count[0]} {channel_type}channels')
        if emission_wavelength is not None:
            print(f'emission_wavelength was set to {emission_wavelength} for {count[1]} {channel_type}channels')
        if exposure_time is not None:
            print(f'exposure_time was set to {exposure_time} for {count[2]} {channel_type}channels')
        
    def from_numpy(self,channel_type: str = '',data: np.ndarray = None, traces_in: Optional[str]='rows', 
                   excitation_wavelength: Optional[float] = None, emission_wavelength: Optional[float] = None, 
                   exposure_time: Optional[float] = None, metadata: Optional[Metadata] = None):
        if traces_in == 'cols' or traces_in == 'columns':
            data = data.T
        elif traces_in != 'rows':
            raise ValueError("traces_in must be one of the following strings: 'rows', 'cols', 'columns'")
        ntraces = len(self.traces)
        if ntraces == 0:
            for index in enumerate(data):
                self.add(Trace(channels=[])) # Populate empty Dataset with empty Trace objects
        elif ntraces != data.shape[0]:
            raise ValueError("Dataset must either be empty or contain the same number of traces as the input array. " + f"Input array contains {ntraces} {traces_in} but Dataset has {data.shape[0]} traces.")
        replace_warning_issued = False
        for index, row in enumerate(data):
            row = row.astype(float).tolist()
            newchannel = Channel(channel_type=channel_type, data=row, excitation_wavelength=excitation_wavelength,
                              emission_wavelength=emission_wavelength,exposure_time=exposure_time,metadata=metadata)
            added = False
            for channel in self.traces[index].channels:
                if channel.channel_type == channel_type:
                    channel = newchannel
                    added = True
                    if replace_warning_issued == False:
                        print(f'Warning: some traces already contained a {channel_type} channel; these were replaced.')
                        replace_warning_issued = True
            if added == False:
                self.traces[index].add(newchannel) 
                        
    def from_csv(self,channel_type: str = '',filename: str = '', traces_in: Optional[str]='rows', 
                   excitation_wavelength: Optional[float] = None, emission_wavelength: Optional[float] = None, 
                   exposure_time: Optional[float] = None, metadata: Optional[Metadata] = None):
        data = np.loadtxt(filename,delimiter=',')
        self.from_numpy(channel_type=channel_type, data=data, traces_in=traces_in, excitation_wavelength=excitation_wavelength,
                        emission_wavelength=emission_wavelength, exposure_time=exposure_time, metadata=metadata)
                    
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

