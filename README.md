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

```python
from accessgap_utils import OverpassQuery

polygon = MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])])
query = OverpassQuery(polygon)
query.request()
```

### Query with tags (filter clauses)

```python
from accessgap_utils import OverpassQuery

polygon = MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])])
query = OverpassQuery(polygon, tags=["[amenity=restaurant]", "[amenity=bar]"])
query.request()
```

By default, the query will return all objects that match **any filter clause** in the list.
The optional `tags` parameter can be a list of clause strings or a single string. Any valid Overpass clause can be passed here, including regular expressions. With clever use of syntax, recursive queries can be constructed. However, please be cautious, as you are responsible for the correctness of the query.

```python
# regex
from accessgap_utils import OverpassQuery

polygon = MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])])
tags = ['[amenity~"restaurant"]', '[amenity~"bar"]']
query = OverpassQuery(polygon, tags=tags)

# returns all objects in the polygon that **either**:
# 1. have `restaurant` in the `amenity` field (not necessarily ['amenity'='restaurant']).
# 2. have `bar` in the `amenity` field (not necessarily ['amenity'='bar']).

query.request()
```

```python
# recurse up
from accessgap_utils import OverpassQuery

polygon = MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])])
tags = "['power=tower']->.search" # recurse up
query = OverpassQuery(polygon, tags=tags)

# returns all objects that:
# 1. have `power=tower` in the `power` field and is in the polygon.
# 2. are connected to the objects in (1) but not necessarily in the polygon.

query.request()
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
