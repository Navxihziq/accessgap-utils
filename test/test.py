import sys
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import pytest
from shapely.geometry import Polygon

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from accessgap_utils import OverpassFilter, OverpassQuery, pois_from_polygon


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


@pytest.mark.overpass_coordstr
def test_overpass_coordstr() -> None:
    """Test if the OverpassFilter.__str__ method is working correctly"""
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    filter = OverpassFilter(polygon)
    assert (
        filter.polygon_coords_str()
        == "0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000"
    )


@pytest.mark.overpass_query
def test_overpass_query() -> None:
    """Test if the OverpassQuery.__str__ method is working correctly"""
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    query = OverpassQuery(polygon)
    assert (
        str(query)
        == "[out:json]; (node(poly:'0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000'); "
        "way(poly:'0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000'); "
        "relation(poly:'0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000');) out body;"
    )


@pytest.mark.overpass_query
def test_overpass_preamble() -> None:
    """Test if the OverpassQuery.__str__ method is working correctly"""
    polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    query = OverpassQuery(polygon, timeout=10, maxsize=10000, date=datetime(2017, 3, 9))
    assert (
        str(query)
        == "[out:json][timeout:10][maxsize:10000][date:'2017-03-09T00:00:00Z']; (node(poly:'0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000'); "
        "way(poly:'0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000'); "
        "relation(poly:'0.000000 0.000000 1.000000 0.000000 1.000000 1.000000 0.000000 1.000000 0.000000 0.000000');) out body;"
    )

