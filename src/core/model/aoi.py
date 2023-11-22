from dataclasses import dataclass
from functools import cached_property
from typing import Tuple

from osgeo.ogr import Geometry


@dataclass
class AOI:
    id: int
    label: str
    geometry: Geometry

    @cached_property
    def envelope(self) -> Tuple[float, float, float, float]:
        """Lazily calculates geometry envelope.

        Returns:
            Geometry envelope.
        """
        return self.geometry.GetEnvelope()

    @cached_property
    def centroid(self) -> Tuple[float, float]:
        """Lazily calculates geometry centroid.

        Returns:
            Geometry centroid.
        """
        x = self.geometry.Centroid().GetX()
        y = self.geometry.Centroid().GetY()
        return (x, y)
