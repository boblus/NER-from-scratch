# sampling
### 1. read configuration files  

nota bene: please put all the configuration files under `formatData/config`  

```python
config_class_features = read_data("config/config-class-features.json")
config_classinfo = read_data("config/config-classinfo.json")
config_numeric_fields = read_data("config/config-numeric-fields.json")
config_dynamic_units = read_data("config/config-dynamic-units.json")
pair_params = read_data("config/pair-params")
```

### 2. initialize *sampling*  

|  |  |  |
|----|----|----|
|**parameters:**|**filename:**|*str*|
| | |the name of a component file (e.g. "Array_Network_Resistors.json")|
| |**p:**|*int*|
| | |the portion of features needs sampling|
| |**most_relevant_p:**|*int*|
| | |the portion of most relevant features in a sample|

*Example:*
```python
rs = sampling("Array_Network_Resistors.json", 0.2, 0.6)
```

### 3. call *random_sampling*  

*Example:*
```python
rs.random_sampling()
```

*Output:*
```
{'Resistors': {'Array Network Resistors': {'Resistance': '51500.0Ohm',
  'SizeCode': '5030',
  'TemperatureCoefficient': '25ppm/°C',
  'RatedPowerDissipationP': '0.575MW',
  'ResistorType': 'ARRAY/NETWORK RESISTOR',
  'PackageLength': '8.6mm',
  'PackageHeight': '1.59mm',
  'NetworkType': 'BUSSED'}}}
```

### 4. concatenate  

*Example:*
```python
text = rs.random_sampling()
connect(rs.sample)
```

*Output:*
```
'101900.0MΩ;6912,METAL GLAZE/THICK FILM,100ppm/°C,-55.0°C,125.0°C,PCB Mount,SPD08A1691GS'
```
