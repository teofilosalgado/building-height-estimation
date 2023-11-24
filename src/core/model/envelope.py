from dataclasses import dataclass
from functools import cached_property

from osgeo import ogr


@dataclass
class Envelope:
    min_x: float
    max_x: float
    min_y: float
    max_y: float

    @cached_property
    def wkt(self) -> str:
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(self.max_y, self.min_x)
        ring.AddPoint(self.min_y, self.min_x)
        ring.AddPoint(self.min_y, self.max_x)
        ring.AddPoint(self.max_y, self.max_x)

        polygon = ogr.Geometry(ogr.wkbPolygon)
        polygon.AddGeometry(ring)
        return polygon.ExportToWkt()
