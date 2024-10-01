"""A module of classes for building Overpass API queries."""

from datetime import datetime
from enum import Enum
from typing import Union

from overpy import Overpass, Result
from shapely.geometry import MultiPolygon, Polygon


class QueryBody:
    """A class for building the body of an Overpass API query."""

    def __init__(
        self,
        polygon: MultiPolygon | Polygon,
        tags: list[str] | str | None = None,
    ) -> None:
        self.polygon = polygon
        self.poly_clause = f"poly:'{self.polygon_coords_str()}'"
        self.tags = [tags] if isinstance(tags, str) else tags

    def query(self) -> str:
        """Build the query body."""

        def nwr_clause(tag_clause: str) -> str:
            return f"node{tag_clause}({self.poly_clause});way{tag_clause}({self.poly_clause});relation{tag_clause}({self.poly_clause});"

        query = []
        if self.tags is None:
            query.append(nwr_clause(""))
        else:
            for tag in self.tags:
                query.append(nwr_clause(tag))

        return "(" + "\n".join(query) + ");"

    def polygon_coords_str(self) -> str:
        """Convert the polygon to a string of coordinates."""
        # convex hull
        assert isinstance(self.polygon, MultiPolygon | Polygon)
        hull = MultiPolygon([self.polygon.convex_hull])
        coords = []
        for geom in hull.geoms:
            x, y = geom.exterior.xy
            coord_ls = [f"{y:.6f} {x:.6f}" for x, y in zip(x, y)]
            coords.append(" ".join(coord_ls))

        return " ".join(coords)


class QueryPreamble:
    def __init__(
        self,
        timeout: int | None = None,
        maxsize: int | None = None,
        date: datetime | None = None,
    ):
        self.timeout = timeout
        self.maxsize = maxsize
        self.date = date

    def query(self) -> str:
        parts = ["[out:json]"]
        if self.timeout is not None:
            parts.append(f"[timeout:{self.timeout}]")
        if self.maxsize is not None:
            parts.append(f"[maxsize:{self.maxsize}]")
        if self.date is not None:
            parts.append(f"""[date:"{self.date.strftime('%Y-%m-%dT%H:%M:%SZ')}"]""")
        return "".join(parts) + ";"


class QuickTags(Enum):
    """Enumeration of allowed quick tags for Overpass queries.

    This enum defines a set of predefined tags commonly used in Overpass queries
    for querying OpenStreetMap data. Each enum member represents a specific
    category or type of place, and contains a list of one or more OSM tags
    associated with that category.

    Available quick tags:
    - RESTAURANT: Queries for restaurants
    - FOOD_COURT: Queries for food courts
    - CAFE: Queries for cafes
    - FAST_FOOD: Queries for fast food establishments
    - BAR: Queries for bars
    - PUB: Queries for pubs
    - ICE_CREAM: Queries for ice cream shops
    - BIERGARTEN: Queries for beer gardens
    - OUTDOOR_SEATING: Queries for outdoor seating areas
    - ALL_FOOD: Queries for all food-related establishments (combines all of the above)

    Each quick tag can be used to simplify the process of querying specific
    types of places without manually specifying the OSM tags.
    """

    RESTAURANT = "[amenity=restaurant]"
    FOOD_COURT = "[amenity=food_court]"
    CAFE = "[amenity=cafe]"
    FAST_FOOD = "[amenity=fast_food]"
    BAR = "[amenity=bar]"
    PUB = "[amenity=pub]"
    ICE_CREAM = "[amenity=ice_cream]"
    BIERGARTEN = "[amenity=biergarten]"
    OUTDOOR_SEATING = "[leisure=outdoor_seating]"

    ALL_FOOD = [
        "[amenity=restaurant]",
        "[amenity=food_court]",
        "[amenity=cafe]",
        "[amenity=fast_food]",
        "[amenity=bar]",
        "[amenity=pub]",
        "[amenity=ice_cream]",
        "[amenity=biergarten]",
        "[leisure=outdoor_seating]",
    ]


class OverpassQuery:
    """A class for building and sending Overpass API queries.

    Args:
        polygon (MultiPolygon | Polygon): The polygon to query.
        quick_tags (QuickTags | str | None): Optional. The quick tags to query.
        customized_filters (list[str] | str | None): Optional. The customized filters to query.
        timeout (int | None): Optional. The timeout for the query in seconds.
        maxsize (int | None): Optional. The maximum size for the query response in bytes.
        date (datetime | None): Optional. The date for attic (historical) data retrieval.

    Examples:
        >>> from accessgap_utils import OverpassQuery
        >>> from datetime import datetime
        >>> polygon = MultiPolygon([Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])])
        >>> query = OverpassQuery(polygon, tags=["amenity=restaurant"], date=datetime(2022, 1, 1))
        >>> print(query.query())
        >>> result = query.request()
        >>> print(result)

    """

    def __init__(
        self,
        polygon: MultiPolygon | Polygon,
        quick_tags: Union[QuickTags, str, None] = None,
        customized_filters: list[str] | str | None = None,
        timeout: int | None = None,
        maxsize: int | None = None,
        date: datetime | None = None,
    ):
        self.preamble = QueryPreamble(timeout, maxsize, date)
        if quick_tags is not None:
            if isinstance(quick_tags, QuickTags):
                self.body = QueryBody(polygon, quick_tags.value)
            else:
                self.body = QueryBody(polygon, QuickTags[quick_tags.upper()].value)
        else:
            self.body = QueryBody(polygon, customized_filters)
        self.epilogue = "out body;"

    def query(self) -> str:
        """Build the query."""
        parts = [self.preamble.query(), self.body.query(), self.epilogue]
        return "".join(parts)

    def request(self) -> Result:
        """Send the query to the Overpass API."""
        api = Overpass()
        return api.query(self.query())
