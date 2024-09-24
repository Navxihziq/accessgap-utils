# AccessGap Utils

Utility functions for Urban Access Gap Project.

## Installation

You can install this package from GitHub using `pip`:

Currently having trouble with wheel dependencies. So for now, install the package separately.

```bash
pip install osmnx pandas geopandas
```

```bash
pip install git+https://github.com/Navxihziq/accessgap-utils.git
```

## Usage

```python
from accessgap_utils import get_points_from_polygon

ri = osmnx.features_from_place('Roosevelt Island, NYC', tags={'place': 'island'})
ri_polygon = gpd.GeoSeries.from_wkt(ri.geometry.iloc[0])
features = get_points_from_polygon(ri_polygon)
```

## Development
