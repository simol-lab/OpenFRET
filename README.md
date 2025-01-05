# OpenFRET Data Format

This repository provides a standardized format for storing single-molecule FRET (Förster Resonance Energy Transfer) data, along with libraries for reading and writing data in this format across multiple programming languages.

## Overview

The OpenFRET data format is defined using OpenAPI 3.0.0. This ensures a clear and unambiguous specification, making it easy to generate parsers and writers in various languages. The core concept is a hierarchical structure containing datasets, traces, and channels, with associated metadata at each level.

## Data Format Specification

The data format is defined in `openfret.yaml`. A summary of the key components is provided below. Keys marked with **(Required)** are mandatory.

*   **Dataset (Required: `title`, `traces`):** The top-level container representing an entire experiment.
    *   `title` **(Required):** Title of the experiment.
    *   `description`: Detailed description of the experiment.
    *   `experiment_type`: Type of experiment (e.g., 2-Color FRET, 3-Color FRET).
    *   `authors`: List of authors.
    *   `institution`: Name of the institution.
    *   `date`: Date of the experiment (YYYY-MM-DD).
    *   `traces` **(Required):** Array of single-molecule traces.
    *   `metadata`: User-defined metadata associated with the dataset.
    * `sample_details`: Details about the sample used in the experiment.
        * `buffer_conditions`: Description of buffer used.
        * `other_details`: Other sample details (metadata).
    * `instrument_details`: Details about the instrument used in the experiment.
        * `microscope`: Microscope model used.
        * `laser`: Laser details.
        * `detector`: Detector details.
        * `other_details`: Other instrument details (metadata).
*   **Trace (Required: `channels`):** Represents a single-molecule measurement over time.
    *   `channels` **(Required):** Array of channel data.
    *   `metadata`: User-defined metadata associated with the trace.
*   **Channel (Required: `channel_type`, `data`):** Represents a single measurement channel (e.g., donor, acceptor).
    *   `channel_type` **(Required):** Identifier for the channel (e.g., donor, acceptor, FRET).
    *   `excitation_wavelength`: Excitation wavelength in nm.
    *   `emission_wavelength`: Emission wavelength in nm.
    *   `exposure_time`: Exposure time per frame in seconds.
    *   `data` **(Required):** Array of intensity values.
    * `metadata`: Metadata for each channel.
*   **Metadata:** A flexible structure for storing user-defined metadata. It allows any key-value pairs.

## Libraries

This repository provides libraries in multiple programming languages to facilitate reading and writing OpenFRET data.

### Python

A Python library is available and published on PyPI. You can install it using pip:

```bash
pip install openfret
```

This library provides functions to load and save data according to the OpenFRET specification.

### C++

A C++ library is also provided for high-performance applications. Instructions on building and using this library will be added in the future.

### Matlab

Matlab functions for reading and writing OpenFRET data are provided in the `matlab/` directory.

*   `openfret.m`: Contains the functions to read and write OpenFRET files.
*   `main.m`: An example script demonstrating how to use the `openfret.m` library.

To use the Matlab library:

1.  Add the `matlab/` folder to your Matlab path.
2.  Use the functions defined in `openfret.m` in your scripts, referring to `main.m` for an example.

### TypeScript

A TypeScript library is available for use in web applications and Node.js environments. Instructions on usage will be added in the future.

## Example

An example of a valid OpenFRET data structure in JSON format:

```json
{
    "title": "My FRET Experiment",
    "traces": [
        {
            "channels": [
                {
                    "channel_type": "donor",
                    "excitation_wavelength": null,
                    "emission_wavelength": null,
                    "exposure_time": null,
                    "data": [
                        100,
                        110,
                        120
                    ],
                    "metadata": {}
                },
                {
                    "channel_type": "acceptor",
                    "excitation_wavelength": null,
                    "emission_wavelength": null,
                    "exposure_time": 0.1,
                    "data": [
                        20,
                        30,
                        40
                    ],
                    "metadata": {
                        "gain": 1.2
                    }
                }
            ],
            "metadata": {
                "trace_condition": "high salt"
            }
        },
        {
            "channels": [
                {
                    "channel_type": "donor",
                    "excitation_wavelength": null,
                    "emission_wavelength": null,
                    "exposure_time": null,
                    "data": [
                        120,
                        110,
                        100
                    ],
                    "metadata": {}
                },
                {
                    "channel_type": "acceptor",
                    "excitation_wavelength": null,
                    "emission_wavelength": null,
                    "exposure_time": null,
                    "data": [
                        40,
                        30,
                        20
                    ],
                    "metadata": {}
                }
            ],
            "metadata": {}
        }
    ],
    "metadata": {},
    "sample_details": {
        "buffer_conditions": "1xPBS"
    },
    "instrument_details": {
        "microscope": "Olympus IX71"
    },
    "description": "FRET experiment on DNA origami",
    "date": "2024-01-01"
}
```

## Contributing

Contributions to this project are welcome! Please open an issue or submit a pull request.

