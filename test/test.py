import sys
from datetime import datetime
from pathlib import Path

import geopandas as gpd
import osmnx as ox
import pytest
from strategy import GREENPOINT, GREENPOINT_POLY_CLAUSE

# Add the parent directory to sys.path to make accessgap_utils visible
sys.path.append(str(Path(__file__).parent.parent))

from accessgap_utils import OverpassQuery


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


@pytest.mark.query_building
def test_preamble_date() -> None:
    """Test if the preamble is working correctly"""
    polygon = GREENPOINT
    date = datetime(2019, 3, 9)
    query = OverpassQuery(polygon, date=date)
    ground_truth = f"""[out:json][date:"{date.strftime('%Y-%m-%dT%H:%M:%SZ')}"];(node{GREENPOINT_POLY_CLAUSE};way{GREENPOINT_POLY_CLAUSE};relation{GREENPOINT_POLY_CLAUSE};);out body;"""
    assert query.query().replace("\n", "") == ground_truth.replace("\n", "")


@pytest.mark.query_building
def test_query_body() -> None:
    """Test if the query body is working correctly"""
    polygon = GREENPOINT
    date = datetime(2019, 3, 9)
    query = OverpassQuery(polygon, date=date, tags="['amenity'='restaurant']")
    ground_truth = f"""[out:json][date:"{date.strftime('%Y-%m-%dT%H:%M:%SZ')}"];(node['amenity'='restaurant']{GREENPOINT_POLY_CLAUSE};way['amenity'='restaurant']{GREENPOINT_POLY_CLAUSE};relation['amenity'='restaurant']{GREENPOINT_POLY_CLAUSE};);out body;"""
    assert query.query().replace("\n", "") == ground_truth.replace("\n", "")


@pytest.mark.query_building
def test_query_body_multiple_tags() -> None:
    """Test if the query body is working correctly with multiple tags"""
    polygon = GREENPOINT
    date = datetime(2019, 3, 9)
    query = OverpassQuery(
        polygon, date=date, tags=["['amenity'='restaurant']", "['amenity'='bar']"]
    )
    ground_truth = f"""[out:json][date:"{date.strftime('%Y-%m-%dT%H:%M:%SZ')}"];(node['amenity'='restaurant']{GREENPOINT_POLY_CLAUSE};way['amenity'='restaurant']{GREENPOINT_POLY_CLAUSE};relation['amenity'='restaurant']{GREENPOINT_POLY_CLAUSE};node['amenity'='bar']{GREENPOINT_POLY_CLAUSE};way['amenity'='bar']{GREENPOINT_POLY_CLAUSE};relation['amenity'='bar']{GREENPOINT_POLY_CLAUSE};);out body;"""
    assert query.query().replace("\n", "") == ground_truth.replace("\n", "")


@pytest.mark.query_rst
def test_query_rst() -> None:
    """Test if the query rst is working correctly"""
    polygon = GREENPOINT
    query = OverpassQuery(polygon, tags="['amenity'='restaurant']")
    print(query.query())
    result = query.request()

    # osmnx
    ox.settings.use_cache = False
    gdf = ox.features_from_polygon(GREENPOINT, tags={"amenity": "restaurant"})
    assert len(gdf.loc["node"]) == len(result.nodes)
    assert len(gdf.loc["way"]) == len(result.ways)
