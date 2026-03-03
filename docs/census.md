# Census API

To proxy for transportation access, we will use the `B08201: Household Size by Vehicles Available` dataset, at the census
tract granularity. Using the api key, we can create a query URL to get exactly what we want. The general shape of that looks
like `https://api.census.gov/data/2024/acs/acs5?get=group(B08201),NAME&for=tract:*&in=state:28&key=api_key`. There are
[122 variables](https://api.census.gov/data/2024/acs/acs5/groups/B08201.html) in this particular dataset.

For example:
```python
import os

api_key = os.getenv('CENSUS_API_KEY')

url = f"https://api.census.gov/data/2024/acs/acs5"

params = {
    'get': 'NAME,B08201_001E,B08201_002E',    # Tract name, Totals, No vehicles
    'for': 'tract:*',                         # All tracts
    'in': 'state:28',                         # In Mississippi (FIPS code 28)
    'key': api_key
}
```

The data is returned in the format of a list of lists, where the first list is the variable names