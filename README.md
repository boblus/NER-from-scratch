# sampling
### 1. initialize *sampling*  

nota bene: please put all the configuration files under `formatData/config`  

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
from sampling import *

s = sampling("Array_Network_Resistors.json", 0.2, 0.6)
```

### 2. call *random_sampling*  

*Example:*
```python
s.random_sampling()
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

### 3. concatenate  

*Example:*
```python
text = s.random_sampling()
connect(s.sample)
```

*Output:*
```
'101900.0MΩ;6912,METAL GLAZE/THICK FILM,100ppm/°C,-55.0°C,125.0°C,PCB Mount,SPD08A1691GS'
```
