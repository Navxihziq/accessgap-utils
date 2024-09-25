from datetime import datetime
from typing import TYPE_CHECKING

import geopandas as gpd
import osmnx as ox
from shapely.geometry import MultiPolygon, Polygon

from accessgap_utils.query import OverpassQuery

if TYPE_CHECKING:
    from osmnx.settings import Settings


class OSMQuerySettings:
    def __init__(self, out_format: str = "json", timeout: int = 90):
        self.out_format = out_format
        self.timeout = timeout

    def set_date(self, date: datetime) -> None:
        """Set the date for historical data retrieval."""
        self.date = date

    def to_string(self) -> str:
        """Convert the settings to a string format for OSM query."""
        return f"[out:{self.out_format}][timeout:{self.timeout}][date:'{self.date.strftime('%Y-%m-%dT%H:%M:%SZ')}']"


def all_points_gdf(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Filter the GeoDataFrame to replace all areas with centroids of the areas"""
    # Check if 'way' geometries exist and are not empty before replacing with centroids
    if "way" in gdf.index and not gdf.loc["way", "geometry"].empty:
        gdf.loc["way", "geometry"] = gdf.loc["way", "geometry"].apply(
            lambda x: x.centroid if not x.is_empty else x
        )

    # Check if 'relation' geometries exist and are not empty before replacing with centroids
    if "relation" in gdf.index and not gdf.loc["relation", "geometry"].empty:
        gdf.loc["relation", "geometry"] = gdf.loc["relation", "geometry"].apply(
            lambda x: x.centroid if not x.is_empty else x
        )

    return gdf


def pois_from_polygon(
    polygon: MultiPolygon | Polygon,
    tags: dict[str, str] | None = None,
    date: datetime | None = None,
    cache: bool = True,
) -> gpd.GeoDataFrame:
    """Retrieve points of interest within a specified polygon.

    This function extracts points of interest from OpenStreetMap data
    based on a given polygon and optional tag filters.

    Args:
        polygon (MultiPolygon | Polygon): The geographical area to search within.
            Can be either a single Polygon or a MultiPolygon. We assume the polygon
        tags (dict[str, str] | None): Key-value pairs for filtering points of interest.
            If None, defaults to {'amenity': 'restaurant'}. The values could be a value or True.
            Example: {'amenity': 'school', 'operator': 'public'}
        date (datetime.datetime | None): Timestamp for historical data retrieval.
            If None, uses the most recent data available.
        cache (bool): Whether to save the requests in the local cache.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the extracted points of interest.
            Each row represents a distinct location with its associated metadata.

    Note:
        The function relies on the OSMnx library to interact with OpenStreetMap data.
        Ensure you have a stable internet connection for data retrieval.

    Example:
        >>> area = box(minx, miny, maxx, maxy)
        >>> poi = get_points_from_polygon(area, tags={'amenity': 'hospital'})

    """
    osm_settings = OSMQuerySettings(out_format="json", timeout=90)
    if tags is None:
        tags = {"amenity": "restaurant"}

    settings: Settings = ox.settings  # Type hint for ox.settings

    if not cache:
        # alter osmnx settings
        settings.use_cache = False
    else:
        settings.use_cache = True

    # TODO: future warning: more than one settings object will be allowed
    if date is not None:
        osm_settings.set_date(date)
        settings.overpass_settings = osm_settings.to_string()

    gdf = ox.features_from_polygon(polygon, tags=tags)
    # replace all ways and relations with their centroids
    gdf = all_points_gdf(gdf)

    return gdf


def overpass_query(
    polygon: MultiPolygon | Polygon,
    tags: dict[str, str] | None = None,
    timeout: int | None = None,
    maxsize: int | None = None,
    date: datetime | None = None,
) -> str:
    return OverpassQuery(polygon, tags, timeout, maxsize, date)
