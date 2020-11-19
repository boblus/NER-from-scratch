#!/usr/bin/env python
# coding: utf-8


import os
import json
import sys
import random
from collections import defaultdict
from typing import Tuple, Dict, Sequence, List, Set


def read_data(filename: str):
    """
    filename: the name of a file
    returns the data of in the file
    """
    directory = "formatData/" + filename
    with open(directory, 'r', encoding='utf-8') as file:
        data = json.loads(file.read())
    return data

def get_keys(d, value):
    return [k for k,v in d.items() if v == value]

def extract_feature_value(filename: str) -> dict:
    """
    filename: the filename of a component (e.g. "Active_Filters.json")
    returns all the features of a component and their corresponding values 
    """
    features_values = defaultdict(set)
    for item in read_data(filename):
        for feature in item:
            features_values[feature].add(item[feature])
    return features_values


def random_sampling(filename: str, config_class_features: dict, config_classinfo: dict, p: float) -> dict:
    """
    filename: the filename of a component (e.g. "Active_Filters.json")
    config_class_features: the configuration info of all components (in "config/config-class-features.json")
    p: the portion of features needs sampling
    returns the sample
    """
    component_name = os.path.splitext(filename)[0].replace("_"," ") # obtain the name of the component
    print(component_name)
    classList = []
    for item in list(config_classinfo.values()):
        for component in item:
            if component == component_name:
                classList.append(get_keys(config_classinfo, item))

    features_values = extract_feature_value(filename)
    features_list = list(features_values.keys())
    sample_size = int(len(features_list) * p)
    
    sample = defaultdict()
    if 'necessary' in config_class_features[classList[0][0]].keys(): # check if the component has a necessary feature
        feature = config_class_features[component_name]['necessary'][0]
        sample[feature] = random.sample(list(features_values[feature]), 1)[0]
        features_list.remove(feature)
        sample_size -= 1
       
    sample_features = random.sample(features_list, sample_size)
    for feature in sample_features:
        sample[feature] = random.sample(list(features_values[feature]), 1)[0]
        
    return sample
