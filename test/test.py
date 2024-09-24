import sys
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import pytest

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from accessgap_utils import pois_from_polygon


def assert_non_empty_gdf(gdf: gpd.GeoDataFrame) -> None:
    """Assert that the GeoDataFrame is not empty"""
    assert len(gdf) > 0


@pytest.mark.osmnx_installation
def test_osmnx_installation() -> None:
    """Test if osmnx is installed correctly"""
    assert ox.__version__ is not None
    # try to get points from address
    gdf = ox.features_from_place(
        "Roosevelt Island, New York", tags={"amenity": "restaurant"}
    )
    assert_non_empty_gdf(gdf)


@pytest.mark.datetime
def test_datetime() -> None:
    """Test if the datetime is working correctly"""
    from datetime import datetime

    date = datetime(2017, 3, 9)
    # get the polygon of the island
    polygon = ox.features_from_place(
        "Roosevelt Island, New York", tags={"place": "island"}
    ).geometry.iloc[0]
    gdf = pois_from_polygon(polygon, date=date, cache=False)
    assert_non_empty_gdf(gdf)
