# sampling

*nota bene:*  
\* please put all the configuration files under `formatData/config`  
\* do not sample on `Analog_Special_Function_Converters.json`, `Carbon_Composition_Resistors.json`, and `Carbon_Film_Resistors.json`

### 1. initialize *sampling*  

|  |  |  |
|----|----|----|
|**parameters:**|**filename:**|*str*|
| | |the name of a component file (e.g. `Array_Network_Resistors.json`)|
| |**most_relevant_p:**|*int*|
| | |the portion of most relevant features in a sample|

*Example:*
```python
from sampling import *

s = sampling("Array_Network_Resistors.json", 0.6)
```

### 2. call *random_sampling*  

*Example:*
```python
s.random_sampling()
```

*Output:*
```
{'class': 'Resistors',
 'category': 'Array Network Resistors',
 'input class': 'res',
 'Resistance': '9790.0O',
 'TemperatureCoefficient': '100ppm/°C',
 'SizeCode': '3040',
 'RatedPowerDissipationP': '1.19uW',
 'NumberofFunctions': '3.0',
 'LeadLength': '4.15',
 'LeadSpacing': '3/5'}
```

### 3. concatenate  

*Example:*
```python
text, text_sep = connect(s.random_sampling())
text
```

*Output:*
```
'101900.0MΩ;6912,METAL GLAZE/THICK FILM,100ppm/°C,-55.0°C,125.0°C,PCB Mount,SPD08A1691GS'
```
