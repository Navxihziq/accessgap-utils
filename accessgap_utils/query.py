from datetime import datetime

from overpy import Overpass, Result
from shapely.geometry import MultiPolygon, Polygon


class QueryBody:
    def __init__(
        self,
        polygon: MultiPolygon | Polygon,
        tags: list[str] | str | None = None,
    ):
        """
        Args:
            polygon: The polygon to query.
            tags: The tags to query. Returns the union of all objects that match any of the tags.
        """
        self.polygon = polygon
        self.poly_clause = f"poly:'{self.polygon_coords_str()}'"
        self.tags = [tags] if isinstance(tags, str) else tags

    def query(self) -> str:
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


class OverpassQuery:
    def __init__(
        self,
        polygon: MultiPolygon | Polygon,
        tags: list[str] | str | None = None,
        timeout: int | None = None,
        maxsize: int | None = None,
        date: datetime | None = None,
    ):
        self.preamble = QueryPreamble(timeout, maxsize, date)
        self.body = QueryBody(polygon, tags)
        self.epilogue = "out body;"

    def query(self) -> str:
        parts = [self.preamble.query(), self.body.query(), self.epilogue]
        return "".join(parts)

    def request(self) -> Result:
        api = Overpass()
        return api.query(self.query())
