# AccessGap Utils

Utility functions for Urban Access Gap Project.

## Installation

You can install this package from GitHub using `pip`. However, due to current issues with wheel dependencies, it's recommended to install the required packages separately before installing the main package.

First, install the necessary dependencies, and then install the main package:

```bash
pip install osmnx pandas geopandas git+https://github.com/Navxihziq/accessgap-utils.git
```

## Usage

```python
from accessgap_utils import get_points_from_polygon

ri = osmnx.features_from_place('Roosevelt Island, NYC', tags={'place': 'island'})
ri_polygon = ri.geometry.iloc[0]
features = get_points_from_polygon(ri_polygon)
```

## Development
