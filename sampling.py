#!/usr/bin/env python
# coding: utf-8

import os
import json
import random
from collections import defaultdict
from typing import Tuple, Dict, Sequence, List, Set


def read_data(filename: str):
    """
    filename: the name of a json file
    returns the data of in the file
    """
    if filename[-5:] == ".json":
        directory = "formatData/" + filename
        with open(directory, 'r', encoding='utf-8') as file:
            data = json.loads(file.read())
    else:
        raise ValueError("The input should be a json file.")
    return data


def extract_feature_value(filename: str) -> dict:
    """
    filename: the filename of a component (e.g. "Active_Filters.json")
    returns all the features of a component and their corresponding values 
    """
    features_values = defaultdict(list)
    for item in read_data(filename):
        for feature in item:
            features_values[feature].append(item[feature])
    return features_values


class sampling():
    def __init__(self, filename: str, config_class_features: dict, config_classinfo: dict, p: float):
        """
        filename: the filename of a component (e.g. "Active_Filters.json")
        config_class_features: the class features info of all components (in "config/config-class-features.json")
        config_classinfo: the class info of all components (in "config/config-classinfo.json")
        p: the portion of features needs sampling
        """
        self.component_name = os.path.splitext(filename)[0].replace("_"," ") # obtain the name of the component (e.g. "Active Filters")
        self.config_class_features = config_class_features
        self.p = p

        self.features_values = extract_feature_value(filename)
        self.features_list = list(self.features_values.keys())

        for key in config_classinfo: # obtain the class of the component (e.g. "Filters")
            if self.component_name in [item.replace("/"," ") for item in config_classinfo[key]]:
                self.component_class = key    

        self.component_config_class_features = list(config_class_features[self.component_class].keys())
    
    def random_sampling(self) -> dict:
        """
        returns a sample
        """
        features_list = self.features_list.copy()
        
        sample_size = int(len(features_list) * self.p)
        if sample_size < 1: # if sample_size is too small, set it to 1
            sample_size = 1
            
        sample = defaultdict()
        if "necessary" in self.component_config_class_features: # check if the component has a necessary feature
            feature = self.config_class_features[self.component_class]['necessary'][0]
            sample[feature] = random.sample(list(self.features_values[feature]), 1)[0] ## TODO: sampling according to distribution
            features_list.remove(feature)
            sample_size -= 1

        if sample_size > 0:   
            sample_features = random.sample(features_list, sample_size)
            for feature in sample_features:
                sample[feature] = random.sample(list(self.features_values[feature]), 1)[0]

        return sample

    
