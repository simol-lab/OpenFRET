classdef openfret
    % OpenFRET A Matlab library for reading and writing OpenFRET data.

    methods (Static)

        function dataset = read(filepath)
            % Reads a Dataset from a JSON file.
            %
            % Args:
            %   filepath (str): Path to the JSON file.
            %
            % Returns:
            %   dataset (struct): The Dataset structure.

            try
                data = jsondecode(fileread(filepath));
            catch ME
                error('OpenFRET:read:JSONError', 'Error decoding JSON file: %s', ME.message);
            end

            dataset = OpenFRET.validateDataset(data);

        end

        function write(dataset, filepath)
            % Writes a Dataset to a JSON file.
            %
            % Args:
            %   dataset (struct): The Dataset structure.
            %   filepath (str): Path to the JSON file.

            dataset = OpenFRET.validateDataset(dataset);
            try
                jsontext = jsonencode(dataset, 'PrettyPrint', true);
                fid = fopen(filepath, 'w');
                fprintf(fid, '%s', jsontext);
                fclose(fid);
            catch ME
                error('OpenFRET:write:JSONError', 'Error encoding or writing JSON file: %s', ME.message);
            end
        end

        function dataset = validateDataset(data)
           % Validates Dataset and its components against the schema.
           % This is a rudimentary check, a full schema validation would be ideal.
           if ~isstruct(data) || ~isfield(data, 'title') || ~isfield(data, 'traces')
               error('OpenFRET:validateDataset:InvalidFormat', 'Dataset must be a struct with fields "title" and "traces".');
           end

           for i = 1:length(data.traces)
               trace = data.traces(i);
               if ~isstruct(trace) || ~isfield(trace, 'channels')
                    error('OpenFRET:validateDataset:InvalidFormat', 'Trace must be a struct with field "channels".');
               end
               for j = 1:length(trace.channels)
                   channel = trace.channels(j);
                   if ~isstruct(channel) || ~isfield(channel, 'channel_type') || ~isfield(channel, 'data')
                       error('OpenFRET:validateDataset:InvalidFormat', 'Channel must be a struct with fields "channel_type" and "data".');
                   end
               end
           end
           dataset = data;
        end
    end
end