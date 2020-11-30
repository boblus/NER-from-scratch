#!/usr/bin/env python
# coding: utf-8

    
import re
import os
import json
import random
from collections import defaultdict
from typing import Tuple, Dict, Sequence, List, Set


def read_data(filename: str):
    """
    filename: the name of a file
    returns the data of in the file
    """
    if filename[-5:] == ".json":
        directory = "formatData/" + filename
        with open(directory, 'r', encoding='utf-8') as file:
            output = json.loads(file.read())
    
    elif filename == "config/pair-params":
        directory = "formatData/" + filename
        with open(directory, 'r', encoding='utf-8') as file:
            data = file.read().split("\n\n")

        output = defaultdict()
        for pair in data:
            pair = pair.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").split("/")
            output[pair[0]] = pair[1]
   
    else:
        raise ValueError("The input is not valid.")
    return output


def preprocess_config_class_features(config_class_features: dict) -> dict:
    """
    config_class_features: the class features of all components (in "config/config-class-features.json")
    returns a preprocessed config-class-features
    """
    output = defaultdict(defaultdict)
    for component in config_class_features:
        for label in config_class_features[component]:
            # "Rated (DC) Voltage (URdc)" in config-class-features appears as "RatedDCVoltageURdc" in a component file
            output[component][label] = [i.replace(" ", "").replace("-", "").replace("(", "").replace(")", "") for i in config_class_features[component][label]]
    return output


def preprocess_config_numeric_fields(config_numeric_fields: list) -> list:
    """
    config_numeric_fields: the numeric fields of all components (in "config/config-numeric-fields.json")
    returns a preprocessed config-class-features
    """
    output = []
    for feature in config_numeric_fields:
        # "Rated (DC) Voltage (URdc)" in config-numeric-fields appears as "RatedDCVoltageURdc" in a component file
        output.append(feature.replace(" ", "").replace("-", "").replace("(", "").replace(")", ""))
    return output


def extract_feature_value(filename: str) -> dict:
    """
    filename: the name of a component file (e.g. "Active_Filters.json")
    returns all the features of a component and their corresponding values 
    """
    features_values = defaultdict(list)
    for item in read_data(filename):
        for feature in item:
            features_values[feature].append(item[feature])
    return features_values


def connect(sample: dict) -> str:
    """
    sample: the output of sampling.random_sampling()
    returns the concatenation of values
    """
    output = ''
    deliminter_list = ['#', ',', '/', ';', ':', '-', '_']
    deliminter = random.sample(deliminter_list, 1)[0]
    for key, value in sample.items():
        if key not in ["class", "category", "input class"]: 
            if random.uniform(0, 1) > 0.9: # 10% chance to use another deliminter
                output = output + str(value) + random.sample(deliminter_list, 1)[0]
            else:
                output = output + str(value) + deliminter
    return re.sub("(" + "|".join(deliminter_list) + ")$", "", output)


class sampling():
    def __init__(
        self,
        filename: str,
        most_relevant_p: float
    ):
        """
        filename: the name of a component file (e.g. "Active_Filters.json")
        most_relevant_p: the portion of most relevant features in a sample
        """
        self.component_name = os.path.splitext(filename)[0].replace("_"," ") # obtain the name of the component (e.g. "Active Filters")
        self.config_class_features = preprocess_config_class_features(config_class_features)
        self.config_numeric_fields = preprocess_config_numeric_fields(config_numeric_fields)
        self.config_class_name_keys = list(config_class_name.keys())
        self.config_dynamic_units_keys = list(config_dynamic_units.keys())
        self.pair_params = pair_params
        self.pair_params_keys = list(pair_params.keys())
        self.pair_params_values = list(pair_params.values())
        
        self.most_relevant_p = most_relevant_p

        self.features_values = extract_feature_value(filename)
        self.features_list = list(self.features_values.keys())

        # obtain the class of the component (e.g. "Filters")
        # component_name "Array Network Resistors" appears as "Array/Network Resistors" in config_classinfo
        for key in config_classinfo:
            if self.component_name in [item.replace("/"," ") for item in config_classinfo[key]]:
                self.component_class = key    

        self.component_config_class_features = list(config_class_features[self.component_class].keys())
        
        # all of the features in config-class-features are not found in component files
        # e.g. "Resistance Law" is not found in Array_Network_Resistors.json
        self.most_relevant_features_list = [i for i in list(self.config_class_features[self.component_class]["Most Relevant"]) if i in self.features_list]
        
        self.units = set()
        self.string_fields = set()
    
    
    def exist_in_pair(self, sample_features: list) -> list:
        """
        sample_features: features need sampling
        returns a new list of sample_features
        """
        output = []
        for feature in sample_features:
            output.append(feature)
            if feature in self.pair_params_keys:
                if random.uniform(0, 1) < 0.9:
                    output.append(self.pair_params[feature])
            if feature in self.pair_params_values:
                if random.uniform(0, 1) < 0.9:
                    inversed_pair_params = {value: key for key, value in self.pair_params.items()}
                    output.append(inversed_pair_params[feature])
        return output

    
    def sample_value(self, sample_features: list):
        """
        sample_features: features need sampling
        """
        for feature in sample_features:
            if feature in self.config_numeric_fields: # check if the feature is numeric
                n = 2
                total_numeric = 0
                for i in range(n):
                    value = str(random.sample(self.features_values[feature], 1)[0])
                    numeric = re.findall("-*\d+\.?\d*", value)[0] # extract the numeric part of the value
                    total_numeric += float(numeric)
                unit = value.strip(numeric) # extract the unit of the value
                total_numeric = total_numeric / n
                
                self.units.add(unit)
                
                # amplify the diversity of unit (e.g. 1000Ω -> 1kΩ)
                if unit in self.config_dynamic_units_keys:
                    new_unit = random.sample(list(config_dynamic_units[unit].keys()), 1)[0]
                    mutator = float(config_dynamic_units[unit][new_unit])
                    
                    self.units.add(new_unit)
                    
                    if mutator < 1:
                        # test if total_numeric is greater than 1/mutator (e.g. normally we do not write 8000mW)
                        while total_numeric >= 1 / mutator: 
                            total_numeric = total_numeric * mutator
                    if mutator > 1:
                        # test if total_numeric is greater than the mutator (e.g. normally we do not write 8000kW)
                        while total_numeric >= mutator: 
                            total_numeric = total_numeric / mutator
                    self.sample[feature] = str(round(total_numeric, 3)) + new_unit
                else:
                    # amplify the diversity of the value (e.g. 0.25W -> 1/4W)
                    if random.uniform(0, 1) < 0.7:
                        self.sample[feature] = str(round(total_numeric, 3)) + unit
                    else:
                        self.sample[feature] = str(random.randint(1, 10)) + "/" + str(random.randint(1, 10)) + unit
            else:
                self.sample[feature] = random.sample(self.features_values[feature], 1)[0]
                self.string_fields.add(random.sample(self.features_values[feature], 1)[0])
    
    
    def random_sampling(self) -> dict:
        """
        returns a sample
        """
        features_list = list(set(self.features_list) - set(self.most_relevant_features_list))
        most_relevant_features_list = self.most_relevant_features_list.copy()
        
        sample_size = int(random.uniform(5, 9)) # sample_size is between 5 and 8
        most_relevant_features_size = int(sample_size * self.most_relevant_p)
            
        self.sample = {"class": self.component_class, "category": self.component_name}
        if self.component_class in self.config_class_name_keys: # check if the component's class is in config_class_name
            if random.uniform(0, 1) < 0.2:
                self.sample["input class"] = "".join(random.sample(config_class_name[self.component_class], 1))
        
        if "necessary" in self.component_config_class_features: # check if the component has a necessary feature
            sample_features = self.config_class_features[self.component_class]["necessary"]
            extended_sample_features = self.exist_in_pair(sample_features)
            self.sample_value(extended_sample_features)
            most_relevant_features_list = list(set(most_relevant_features_list) - set(extended_sample_features))
            sample_size -= len(sample_features)
            most_relevant_features_size -= len(sample_features)
            
        if most_relevant_features_size > 0:
            if len(most_relevant_features_list) >= most_relevant_features_size:
                sample_features = random.sample(most_relevant_features_list, most_relevant_features_size)
            else:
                sample_features = random.sample(most_relevant_features_list, len(most_relevant_features_list))
            extended_sample_features = self.exist_in_pair(sample_features)
            self.sample_value(extended_sample_features)
            sample_size -= most_relevant_features_size

        if sample_size > 0:   
            sample_features = random.sample(features_list, sample_size)
            extended_sample_features = self.exist_in_pair(sample_features)
            self.sample_value(extended_sample_features)
        
        return self.sample


config_class_features = read_data("config/config-class-features.json")
config_class_name = read_data("config/config-class-name.json")
config_classinfo = read_data("config/config-classinfo.json")
config_numeric_fields = read_data("config/config-numeric-fields.json")
config_dynamic_units = read_data("config/config-dynamic-units.json")
pair_params = read_data("config/pair-params")
