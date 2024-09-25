# AccessGap Utils

This package primarily serves as an `Overpy` wrapper, facilitating queries for OSM objects based on a given polygon and additional optional parameters.

Reasons for choosing `Overpy` over `OSMnx`:

1. Support for regular expressions.
2. (Potential) Support for historical (attic) data retrieval.

## Installation

You can install this package from GitHub using `pip`. However, due to current issues with wheel dependencies, it's recommended to install the required packages separately before installing the main package.

First, install the necessary dependencies, and then install the main package:

```bash
pip install osmnx pandas geopandas git+https://github.com/Navxihziq/accessgap-utils.git
```

## Usage

```python
from accessgap_utils import pois_from_polygon

ri = osmnx.features_from_place('Roosevelt Island, NYC', tags={'place': 'island'})
ri_polygon = ri.geometry.iloc[0]
features = pois_from_polygon(ri_polygon)
```

### Specifying date for historical (attic) data

```python
from accessgap_utils import pois_from_polygon
from datetime import datetime

ri = osmnx.features_from_place('Roosevelt Island, NYC', tags={'place': 'island'})
ri_polygon = ri.geometry.iloc[0]
features = pois_from_polygon(ri_polygon, date=datetime(2019, 3, 9))
```

## Development
