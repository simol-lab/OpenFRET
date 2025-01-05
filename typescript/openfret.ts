// Typescript library for handling openFRET data format.

export interface Metadata {
  [key: string]: any;
}

export interface Channel {
  channel_type: string;
  excitation_wavelength?: number;
  emission_wavelength?: number;
  exposure_time?: number;
  data: number[];
  metadata?: Metadata;
}

export interface Trace {
  channels: Channel[];
  metadata?: Metadata;
}

export interface SampleDetails {
    buffer_conditions?: string;
    other_details?: Metadata;
}

export interface InstrumentDetails {
    microscope?: string;
    laser?: string;
    detector?: string;
    other_details?: Metadata;
}

export interface Dataset {
  title: string;
  description?: string;
  experiment_type?: string;
  authors?: string[];
  institution?: string;
  date?: string; // Should be a date string (YYYY-MM-DD)
  traces: Trace[];
  metadata?: Metadata;
  sample_details?: SampleDetails
  instrument_details?: InstrumentDetails
}

export class OpenFRET {
  static validateDataset(data: any): Dataset | null {
    try {
      // Basic type checking (can be improved with more robust validation)
      if (typeof data !== 'object' || data === null || !data.title || !data.traces || !Array.isArray(data.traces)) {
        return null;
      }

      const dataset: Dataset = {
        title: data.title,
        description: data.description,
        experiment_type: data.experiment_type,
        authors: data.authors,
        institution: data.institution,
        date: data.date,
        traces: [],
        metadata: data.metadata,
        sample_details: data.sample_details as SampleDetails,
        instrument_details: data.instrument_details as InstrumentDetails
      };

      for (const traceData of data.traces) {
        if (typeof traceData !== 'object' || traceData === null || !traceData.channels || !Array.isArray(traceData.channels)) {
          return null;
        }

        const trace: Trace = { channels: [], metadata: traceData.metadata };
        dataset.traces.push(trace);

        for (const channelData of traceData.channels) {
            if (typeof channelData !== 'object' || channelData === null || !channelData.channel_type || !channelData.data || !Array.isArray(channelData.data)) {
                return null;
            }
            const channel: Channel = {
              channel_type: channelData.channel_type,
              excitation_wavelength: channelData.excitation_wavelength,
              emission_wavelength: channelData.emission_wavelength,
              exposure_time: channelData.exposure_time,
              data: channelData.data,
              metadata: channelData.metadata
            }
            trace.channels.push(channel)
        }
      }

      return dataset;
    } catch (error) {
      console.error("Error during validation:", error);
      return null;
    }
  }

  static toJson(dataset: Dataset): string {
    return JSON.stringify(dataset, null, 2); // Pretty print
  }

  static fromJson(jsonString: string): Dataset | null {
    try {
      const data = JSON.parse(jsonString);
      return OpenFRET.validateDataset(data);
    } catch (error) {
      console.error("Error parsing JSON:", error);
      return null;
    }
  }
}