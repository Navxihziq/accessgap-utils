# AccessGap Utils

Utility functions for Urban Access Gap Project.

## Installation

You can install this package from GitHub using `pip`:

```bash
pip install git+https://github.com/Navxihziq/accessgap-utils.git
```

## Usage

```python
from accessgap_utils import get_points_from_polygon

polygon = gpd.read_file("path/to/polygon.geojson")
features = get_points_from_polygon(polygon)
```

## Development
