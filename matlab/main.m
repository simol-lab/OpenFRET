% Create a sample dataset
save_name = 'fret_data.json';

dataset.title = 'My FRET Experiment';
dataset.description = 'Example FRET data';
dataset.experiment_type = '2-Color FRET';
dataset.authors = {'John Doe', 'Jane Smith'};
dataset.institution = 'University X';
dataset.date = '2024-10-27';
dataset.metadata.experiment_id = '12345'; % Example metadata
dataset.sample_details.buffer_conditions = 'Phosphate Buffer';
dataset.sample_details.other_details.temperature = '25C';
dataset.instrument_details.microscope = 'Olympus IX71';
dataset.instrument_details.laser = '640nm and 532nm lasers';
dataset.instrument_details.detector = 'EMCCD Camera';
dataset.instrument_details.other_details.objective = '100x';

trace1.channels(1).channel_type = 'donor';
trace1.channels(1).data = rand(1, 100);
trace1.channels(1).excitation_wavelength = 532;
trace1.channels(1).emission_wavelength = 580;
trace1.channels(2).channel_type = 'acceptor';
trace1.channels(2).data = rand(1, 100);
trace1.channels(2).excitation_wavelength = 532;
trace1.channels(2).emission_wavelength = 680;
trace1.metadata.trace_id = 'trace001';

trace2.channels(1).channel_type = 'donor';
trace2.channels(1).data = rand(1, 100);
trace2.channels(1).excitation_wavelength = 532;
trace2.channels(1).emission_wavelength = 580;
trace2.channels(2).channel_type = 'acceptor';
trace2.channels(2).data = rand(1, 100);
trace2.channels(2).excitation_wavelength = 532;
trace2.channels(2).emission_wavelength = 680;
trace2.metadata.trace_id = 'trace002';

dataset.traces = [trace1, trace2];

% Write the dataset to a JSON file
openfret.write_data(dataset, save_name);


% Read dataset from a JSON file
load_name = 'fret_data.json';

loaded_dataset = openfret.read_data(load_name);

% Compare the original and loaded datasets (basic check)
if isequal(dataset.title, loaded_dataset.title)
    disp('Success! Dataset was created and loaded.');
else
    disp('Error: Something went wrong. Check that the save name and load name are identical.')
end