# AccessGap Utils

This package primarily serves as an `Overpy` wrapper, facilitating queries for OSM objects based on a given polygon and additional optional parameters.

Please note that this package and the project is still in very early development. PRs, issues and feedback are highly appreciated!

Reasons for choosing `Overpy` over `OSMnx`:

1. Support for regular expressions.
2. (Potential) Support for historical (attic) data retrieval.

## Installation

You can install this package from GitHub using `pip`.

```
pip install git+https://github.com/Navxihziq/accessgap-utils.git
```

## Usage

Here we use `Roosevelt Island` as an example polygon. To get the `MultiPolygon` object, we can use the `features_from_place` function from `OSMnx`.

```python
from osmnx import features_from_place

polygon = features_from_place("Roosevelt Island, New York, USA", tags={"place": "island"}).geometry.iloc[0]
```

```python
>>> from accessgap_utils import OverpassQuery

>>> query = OverpassQuery(polygon)
>>> results = query.request()
>>> len(results.nodes)
    6901

>>> results.nodes[0].tags
    {'amenity': 'restaurant',
      'cuisine': 'japanese',
      'name': 'Fuji East Restaurant',
      'opening_hours': 'Mo-Su 11:00-23:00',
      'outdoor_seating': 'yes'}
```

### Query with tags (filter clauses)

```python
>>> query = OverpassQuery(polygon, customized_filters=["[amenity=restaurant]", "[amenity=bench]"])
>>> results = query.request()
>>> nodes = results.nodes
>>> len(nodes)
    65
>>> nodes[0].tags
    {'amenity': 'restaurant',
    'cuisine': 'japanese',
    'name': 'Fuji East Restaurant',
    'opening_hours': 'Mo-Su 11:00-23:00',
    'outdoor_seating': 'yes'}
>>> nodes[10].tags
    {'amenity': 'bench'}
```

By default, the query will return all objects that match **any filter clause** in the list.
The optional `tags` parameter can be a list of clause strings or a single string. Any valid Overpass clause can be passed here, including regular expressions. With clever use of syntax, recursive queries can be constructed. However, please be cautious, as you are responsible for the correctness of the query.

```python
# multiple tags for AND
>>> query = OverpassQuery(polygon, customized_filters=["[amenity=restaurant][cuisine=italian]"])
>>> results = query.request() # sanity check: only one pizza place on the island
>>> len(results.nodes)  # yay!
    1
>>> results.nodes[0].tags
    {'addr:housenumber': '455',
    'addr:street': 'Main Street',
    'amenity': 'restaurant',
    'cuisine': 'italian',
    'diet:vegetarian': 'yes',
    'drink:beer': 'yes',
    'drink:wine': 'yes',
    'name': 'Piccolo Trattoria',
    'outdoor_seating': 'yes',
    'phone': '+1 212-753-2300',
    'takeaway': 'yes'}
```

However, there is an important caveat: when you specify multiple attributes for the same key, the query will return objects that match **any** of the attributes instead of **all** of them. This behavior may not be intuitive, as it doesn't align with logical expectations. For instance, in the context of OpenStreetMap (OSM), a place typically cannot be both a restaurant and a bar simultaneously.

```python
# multiple tags for AND
>>> query = OverpassQuery(polygon, customized_filters=["[amenity=restaurant][amenity=bench]"])
>>> results = query.request()
>>> len(results.nodes)
    63
```

```python
# regex
>>> tags = ['[amenity~e]']
>>> query = OverpassQuery(polygon, customized_filters=tags)
>>> # returns all objects in the polygon that **either**:
>>> # 1. have `e` in the `amenity` field (not necessarily ['amenity'='e']).
>>> rst = query.request()
>>> len(rst.nodes)
    102
>>> rst.nodes[10].tags
   {'amenity': 'vending_machine', 'fee': 'no', 'vending': 'excrement_bags'}
```

## Development

To set up the development environment, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/your-username/accessgap-utils.git
   cd accessgap-utils
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package with development dependencies:
   ```
   pip install -e ".[dev]"
   ```

This will install the package in editable mode (`-e`) along with all the development dependencies specified in the `extras_require` section of `setup.py`.

4. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

Now you're ready to start developing and contributing to the project!
