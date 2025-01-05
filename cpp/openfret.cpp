// C++ library for handling openFRET data format.

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

// Metadata class
class Metadata : public std::map<std::string, json> {
public:
    friend void to_json(json& j, const Metadata& m);
    friend void from_json(const json& j, Metadata& m);
};

void to_json(json& j, const Metadata& m) {
    for (const auto& pair : m) {
        j[pair.first] = pair.second;
    }
}

void from_json(const json& j, Metadata& m) {
    for (json::const_iterator it = j.begin(); it != j.end(); ++it) {
        m[it.key()] = it.value();
    }
}

// Channel class
struct Channel {
    std::string channel_type;
    float excitation_wavelength = 0.0f;
    float emission_wavelength = 0.0f;
    float exposure_time = 0.0f;
    std::vector<float> data;
    Metadata metadata;

    friend void to_json(json& j, const Channel& c);
    friend void from_json(const json& j, Channel& c);
};

void to_json(json& j, const Channel& c) {
    j = json{{"channel_type", c.channel_type}, {"data", c.data}, {"metadata", c.metadata}};
    if (c.excitation_wavelength != 0.0f) j["excitation_wavelength"] = c.excitation_wavelength;
    if (c.emission_wavelength != 0.0f) j["emission_wavelength"] = c.emission_wavelength;
    if (c.exposure_time != 0.0f) j["exposure_time"] = c.exposure_time;
}

void from_json(const json& j, Channel& c) {
    j.at("channel_type").get_to(c.channel_type);
    j.at("data").get_to(c.data);
    if (j.contains("excitation_wavelength")) j.at("excitation_wavelength").get_to(c.excitation_wavelength);
    if (j.contains("emission_wavelength")) j.at("emission_wavelength").get_to(c.emission_wavelength);
    if (j.contains("exposure_time")) j.at("exposure_time").get_to(c.exposure_time);
    if (j.contains("metadata")) j.at("metadata").get_to(c.metadata);
}


// Trace class
struct Trace {
    std::vector<Channel> channels;
    Metadata metadata;

    friend void to_json(json& j, const Trace& t);
    friend void from_json(const json& j, Trace& t);
};

void to_json(json& j, const Trace& t) {
    j = json{{"channels", t.channels}, {"metadata", t.metadata}};
}

void from_json(const json& j, Trace& t) {
    j.at("channels").get_to(t.channels);
    if (j.contains("metadata")) j.at("metadata").get_to(t.metadata);
}

// Dataset class
struct Dataset {
    std::string title;
    std::string description;
    std::string experiment_type;
    std::vector<std::string> authors;
    std::string institution;
    std::string date;
    std::vector<Trace> traces;
    Metadata metadata;
    struct SampleDetails {
        std::string buffer_conditions;
        Metadata other_details;
                friend void to_json(json& j, const SampleDetails& sd);
        friend void from_json(const json& j, SampleDetails& sd);
    } sample_details;
    struct InstrumentDetails {
        std::string microscope;
        std::string laser;
        std::string detector;
        Metadata other_details;
                friend void to_json(json& j, const InstrumentDetails& id);
        friend void from_json(const json& j, InstrumentDetails& id);
    } instrument_details;

    friend void to_json(json& j, const Dataset& d);
    friend void from_json(const json& j, Dataset& d);
};

void to_json(json& j, const Dataset& d) {
    j = json{
        {"title", d.title},
        {"traces", d.traces},
        {"metadata", d.metadata},
        {"sample_details", d.sample_details},
        {"instrument_details", d.instrument_details}
    };
    if (!d.description.empty()) j["description"] = d.description;
    if (!d.experiment_type.empty()) j["experiment_type"] = d.experiment_type;
    if (!d.authors.empty()) j["authors"] = d.authors;
    if (!d.institution.empty()) j["institution"] = d.institution;
    if (!d.date.empty()) j["date"] = d.date;

}

void from_json(const json& j, Dataset& d) {
    j.at("title").get_to(d.title);
    j.at("traces").get_to(d.traces);
    if (j.contains("description")) j.at("description").get_to(d.description);
    if (j.contains("experiment_type")) j.at("experiment_type").get_to(d.experiment_type);
    if (j.contains("authors")) j.at("authors").get_to(d.authors);
    if (j.contains("institution")) j.at("institution").get_to(d.institution);
    if (j.contains("date")) j.at("date").get_to(d.date);
    if (j.contains("metadata")) j.at("metadata").get_to(d.metadata);
        if (j.contains("sample_details")) j.at("sample_details").get_to(d.sample_details);
        if (j.contains("instrument_details")) j.at("instrument_details").get_to(d.instrument_details);
}

void to_json(json& j, const Dataset::SampleDetails& sd) {
        j = json{{"other_details", sd.other_details}};
        if (!sd.buffer_conditions.empty()) j["buffer_conditions"] = sd.buffer_conditions;
}

void from_json(const json& j, Dataset::SampleDetails& sd) {
        if (j.contains("buffer_conditions")) j.at("buffer_conditions").get_to(sd.buffer_conditions);
        if (j.contains("other_details")) j.at("other_details").get_to(sd.other_details);
}

void to_json(json& j, const Dataset::InstrumentDetails& id) {
        j = json{{"other_details", id.other_details}};
        if (!id.microscope.empty()) j["microscope"] = id.microscope;
        if (!id.laser.empty()) j["laser"] = id.laser;
        if (!id.detector.empty()) j["detector"] = id.detector;
}

void from_json(const json& j, Dataset::InstrumentDetails& id) {
        if (j.contains("microscope")) j.at("microscope").get_to(id.microscope);
        if (j.contains("laser")) j.at("laser").get_to(id.laser);
        if (j.contains("detector")) j.at("detector").get_to(id.detector);
        if (j.contains("other_details")) j.at("other_details").get_to(id.other_details);
}

// Read from JSON file
Dataset read_dataset(const std::string& filename) {
    std::ifstream f(filename);
    json j;
    f >> j;
    Dataset dataset;
    from_json(j, dataset);
    return dataset;
}

// Write to JSON file
void write_dataset(const Dataset& dataset, const std::string& filename) {
    json j = dataset;
    std::ofstream f(filename);
    f << std::setw(4) << j << std::endl; // Use setw for pretty printing
}

int main() {
    // Example usage
    Dataset dataset;
    dataset.title = "My FRET Experiment";
        dataset.sample_details.buffer_conditions = "Test Buffer";
    dataset.traces.resize(1);
    dataset.traces[0].channels.resize(2);
    dataset.traces[0].